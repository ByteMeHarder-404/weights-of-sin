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
CORS(app)

def calculate_cosine_similarity(v1, v2):
    v1, v2 = np.array(v1), np.array(v2)
    dot_product = np.dot(v1, v2)
    norm_v1, norm_v2 = np.linalg.norm(v1), np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0: return 0.0
    return dot_product / (norm_v1 * norm_v2)

@app.route('/recommend', methods=['POST'])
def recommend_endpoint():
    try:
        data = request.get_json()
        title, abstract = data['title'], data['abstract']
        if not title or not abstract:
            return jsonify({"error": "Request must include 'title' and 'abstract'."}), 400
    except Exception:
        return jsonify({"error": "Invalid JSON format."}), 400

    # STAGE 1: Keyword Extraction (Local and Sanitized)
    combined_text = title + " " + abstract
    keywords = extract_keywords_from_text(combined_text)
    
    print(f"\n--- DEBUG: Final Sanitized Keywords for Search: {keywords} ---\n")
    
    if not keywords:
        return jsonify({"error": "Could not extract concepts from the text."}), 400
    
    # STAGE 2: Top Author and Journal Candidate Retrieval
    top_authors = fetch_top_authors_for_concepts(keywords)
    journal_candidates = fetch_journal_candidates(keywords)

    if not journal_candidates:
        return jsonify({"topAuthors": [author.to_dict() for author in top_authors], "journalRecommendations": []}), 200

    # STAGE 3: Semantic Ranking of Journals
    journal_texts = [f"{c.name}. Concepts: {', '.join(c.concepts)}" for c in journal_candidates]
    all_embeddings = get_semantic_embeddings([abstract] + journal_texts)
    user_embedding, journal_embeddings = all_embeddings[0], all_embeddings[1:]

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
            "peer_review_questions": questions
        })

    # STAGE 5: Assemble Final Response
    final_response = {
        "topAuthors": [author.to_dict() for author in top_authors],
        "journalRecommendations": final_journal_recommendations
    }

    return jsonify(final_response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, debug=True)