# filename: app_lite.py
# Dynamic Flask server that fetches real journal recommendations using Gemini and OpenAlex APIs
# This provides live data without the heavy ML dependencies

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3001"]}}, supports_credentials=True)

# --- Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENALEX_BASE_URL = "https://api.openalex.org"
USER_EMAIL = os.getenv("YOUR_EMAIL", "user@example.com")
HEADERS = {"User-Agent": f"JournalCompass/v1.0 ({USER_EMAIL})"}

@app.route('/recommend', methods=['POST'])
def recommend_endpoint():
    print("\n=== New Dynamic Recommendation Request ===")
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided."}), 400
            
        title = data.get('title')
        abstract = data.get('abstract')
        
        if not title or not abstract:
            return jsonify({"error": "Request must include 'title' and 'abstract'."}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid JSON format: {str(e)}"}), 400

    # STAGE 1: Use Gemini to generate keywords for search
    print(f"--- Calling Gemini to extract keywords ---")
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY not found in .env file."}), 500

    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"Extract the 5 most important and distinct academic concepts or keywords from the following title and abstract. Return them as a simple comma-separated list. Title: {title}\nAbstract: {abstract}"
    
    try:
        gemini_response = requests.post(gemini_url, json={"contents": [{"parts": [{"text": prompt}]}]})
        gemini_response.raise_for_status()
        gemini_data = gemini_response.json()
        keywords_text = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
        keywords_list = [kw.strip() for kw in keywords_text.split(',')]
        search_query = " OR ".join(keywords_list)
        print(f"--- Keywords from Gemini: {search_query} ---")
    except Exception as e:
        print(f"ERROR calling Gemini API: {str(e)}")
        return jsonify({"error": "Failed to extract keywords using Gemini.", "details": str(e)}), 500

    # STAGE 2: Use OpenAlex to fetch journal and author data
    print(f"--- Calling OpenAlex with search: {search_query} ---")
    openalex_url = f"{OPENALEX_BASE_URL}/works"
    params = {
        "search": search_query,
        "per-page": 5,
        "filter": "host_venue.type:journal,has_abstract:true",
        "sort": "relevance_score:desc"
    }
    
    try:
        openalex_response = requests.get(openalex_url, params=params, headers=HEADERS)
        openalex_response.raise_for_status()
        openalex_data = openalex_response.json()
    except Exception as e:
        print(f"ERROR calling OpenAlex API: {str(e)}")
        return jsonify({"error": "Failed to fetch data from OpenAlex.", "details": str(e)}), 500

    # STAGE 3: Format the response to match frontend expectations
    top_authors = []
    journal_recommendations = []
    seen_authors = set()
    seen_journals = set()

    for i, work in enumerate(openalex_data.get("results", [])):
        # Format Journal Recommendations
        journal_info = work.get("host_venue", {})
        journal_id = journal_info.get("id")
        
        if journal_id and journal_id not in seen_journals:
            seen_journals.add(journal_id)
            journal_recommendations.append({
                "rank": len(journal_recommendations) + 1,
                "name": journal_info.get("display_name", "N/A"),
                "url": journal_info.get("homepage_url", "#"),
                "publisher": journal_info.get("publisher", "N/A"),
                "semantic_score": round(work.get("relevance_score", 0) / 100, 2), # Normalize score
                "peer_review_questions": [ # Placeholder questions
                    "How does this methodology improve upon existing work in the field?",
                    "What are the key limitations of this study?",
                    "What are the broader implications of these findings?"
                ],
                "issn": journal_info.get("issn_l", "N/A"),
                "impact_factor": 0, # Not directly available
                "acceptance_rate": 0 # Not directly available
            })

        # Format Top Authors
        for authorship in work.get("authorships", []):
            author_info = authorship.get("author", {})
            author_id = author_info.get("id")
            if author_id and author_id not in seen_authors:
                seen_authors.add(author_id)
                top_authors.append({
                    "name": author_info.get("display_name", "N/A"),
                    "institution": (author_info.get("last_known_institution") or {}).get("display_name", "N/A"),
                    "works_count": author_info.get("works_count", 0),
                    "cited_by_count": author_info.get("cited_by_count", 0),
                    "openalex_url": author_info.get("id", "#")
                })
    
    final_response = {
        "topAuthors": top_authors[:5], # Limit to 5 unique authors
        "journalRecommendations": journal_recommendations[:3] # Limit to 3 unique journals
    }

    print(f"--- Successfully assembled dynamic response. ---")
    return jsonify(final_response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    print(f"Starting DYNAMIC lite Flask server on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)