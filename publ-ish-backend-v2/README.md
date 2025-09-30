# Publ-ish AI Journal Recommender v2

This is the complete backend for the advanced Publ-ish AI Journal Recommender. This version includes powerful new features: "Top Author Discovery" and AI-generated "Reverse Peer Review" questions.

## Features

-   **Semantic Search:** Finds the top 3 journals with the highest conceptual similarity to a research abstract.
-   **Top Author Discovery:** Identifies and ranks the most influential authors in the paper's specific domain.
-   **Reverse Peer Review (RAG):** For each recommended journal, a Large Language Model (Gemini) acts as a senior reviewer, generating critical questions a real peer reviewer might ask, based on the journal's recent publications.

## Setup Instructions

### 1. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys
a. Rename the example environment file: `mv .env.example .env`
b. Open the `.env` file and add your credentials for Google Gemini and a valid email for the OpenAlex API.

### 4. Run the Server
```bash
python app.py
```

The server will start, load the ML models, and be available at http://127.0.0.1:5001.

## API Endpoint

### POST /recommend

**URL:** http://127.0.0.1:5001/recommend

**Method:** POST

**Body (JSON):**
```json
{
  "title": "Your Research Paper Title",
  "abstract": "The full abstract of your research paper goes here."
}
```

**Success Response (200 OK):**
```json
{
  "topAuthors": [
    {
      "name": "Geoffrey Hinton",
      "institution": "University of Toronto",
      "works_count": 500,
      "cited_by_count": 800000,
      "openalex_url": "https://openalex.org/A..."
    }
  ],
  "journalRecommendations": [
    {
      "rank": 1,
      "name": "Journal of Machine Learning Research",
      "url": "http://jmlr.org/",
      "publisher": "Microtome Publishing",
      "semantic_score": 0.92,
      "peer_review_questions": [
        "How does your proposed methodology compare to the state-of-the-art models recently published in this journal, specifically regarding computational efficiency?",
        "What are the limitations of your dataset, and how might they affect the generalizability of your findings to real-world scenarios?",
        "Can you elaborate on the theoretical contribution of your work beyond the incremental improvement in performance metrics?"
      ]
    }
  ]
}
