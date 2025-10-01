# filename: app.py

import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# --- Component Imports ---
from core.nlp_service import extract_keywords_from_text, get_semantic_embeddings
from core.openalex_service import fetch_journal_candidates, fetch_top_authors_for_concepts, fetch_recent_abstracts_for_journal
from core.rag_service import generate_peer_review_questions

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}}, supports_credentials=True)

def calculate_cosine_similarity(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    dot_product = np.dot(v1, v2)
    norm_v1, norm_v2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0: return 0.0
    return dot_product / (norm_v1 * norm_v2)

@app.route('/recommend', methods=['POST'])
def recommend_endpoint():
    print("\n=== New Recommendation Request ===")
    try:
        print("Headers:", dict(request.headers))
        data = request.get_json()
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({"error": "No data provided."}), 400
            
        print("Received data:", data)
        title = data.get('title')
        abstract = data.get('abstract')
        
        if not title or not abstract:
            print(f"ERROR: Missing required fields. Title: {bool(title)}, Abstract: {bool(abstract)}")
            return jsonify({"error": "Request must include 'title' and 'abstract'."}), 400
    except Exception as e:
        print(f"ERROR parsing request: {str(e)}")
        return jsonify({"error": "Invalid JSON format."}), 400

    # STAGE 1: Keyword Extraction (Local and Sanitized)
    combined_text = title + " " + abstract
    keywords = extract_keywords_from_text(combined_text)
    
    print(f"\n--- DEBUG: Final Sanitized Keywords for Search: {keywords} ---\n")
    
    if not keywords:
        return jsonify({"error": "Could not extract concepts from the text."}), 400
    
    # STAGE 2: Top Author and Journal Candidate Retrieval
    try:
        top_authors = fetch_top_authors_for_concepts(keywords)
        print(f"Successfully fetched {len(top_authors)} top authors")
    except Exception as e:
        print(f"ERROR fetching top authors: {str(e)}")
        top_authors = []

    try:
        journal_candidates = fetch_journal_candidates(keywords)
        print(f"Successfully fetched {len(journal_candidates)} journal candidates")
    except Exception as e:
        print(f"ERROR fetching journal candidates: {str(e)}")
        return jsonify({"error": "Failed to fetch journal recommendations. Please try again."}), 500

    if not journal_candidates:
        return jsonify({"topAuthors": [author.to_dict() for author in top_authors], "journalRecommendations": []}), 200

    # STAGE 3: Semantic Ranking of Journals
    try:
        journal_texts = [f"{c.name}. Concepts: {', '.join(c.concepts)}" for c in journal_candidates]
        all_embeddings = get_semantic_embeddings([abstract] + journal_texts)
        if not all_embeddings or len(all_embeddings) < 2:
            print("ERROR: Failed to generate embeddings")
            return jsonify({"error": "Failed to analyze paper content. Please try again."}), 500
            
        user_embedding, journal_embeddings = all_embeddings[0], all_embeddings[1:]
        print(f"Successfully generated embeddings for {len(journal_embeddings)} journals")
    except Exception as e:
        print(f"ERROR in semantic ranking: {str(e)}")
        return jsonify({"error": "Failed to analyze paper similarity. Please try again."}), 500

    ranked_results = []
    for i, candidate in enumerate(journal_candidates):
        score = calculate_cosine_similarity(user_embedding, journal_embeddings[i])
        ranked_results.append({"score": score, "candidate": candidate})
    
    ranked_results.sort(key=lambda x: x['score'], reverse=True)

    # STAGE 4: RAG for Reverse Peer Review Questions
    final_journal_recommendations = []
    for i, result in enumerate(ranked_results[:3]):
        candidate = result['candidate']
        recent_abstracts = fetch_recent_abstracts_for_journal(candidate.id)
        questions = generate_peer_review_questions(abstract, candidate, recent_abstracts)
        
        final_journal_recommendations.append({
            "rank": i + 1,
            "name": candidate.name,
            "url": candidate.url,
            "publisher": candidate.publisher,
            "semantic_score": round(result['score'], 2),
            "peer_review_questions": questions,
            "issn": candidate.issn,
            "impact_factor": candidate.impact_factor,
            "acceptance_rate": candidate.acceptance_rate
        })

    # STAGE 5: Assemble Final Response
    final_response = {
        "topAuthors": [author.to_dict() for author in top_authors],
        "journalRecommendations": final_journal_recommendations
    }

    return jsonify(final_response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    debug_mode = os.environ.get("FLASK_ENV") == "development"
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
