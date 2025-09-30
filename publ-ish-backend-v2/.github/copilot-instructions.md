# Publ-ish Backend v2: AI Agent Coding Instructions

## Project Architecture
- **Entry Point:** `app.py` (Flask server, main API logic)
- **Core Services:**
  - `core/nlp_service.py`: Local keyword extraction (YAKE), semantic embeddings (sentence-transformers)
  - `core/openalex_service.py`: Journal and author discovery via OpenAlex API
  - `core/rag_service.py`: Reverse peer review question generation using Google Gemini LLM
  - `core/data_contracts.py`: Data models for journals and authors (dataclasses)

## Data Flow
- `/recommend` endpoint: Receives title/abstract → extracts keywords → fetches top authors/journals → generates peer review questions (RAG)
- All cross-service calls use explicit function imports; data passed as Python objects (dataclasses)

## Developer Workflows
- **Setup:**
  - Create venv: `python3 -m venv venv` (Windows: `.\venv\Scripts\activate`)
  - Install: `pip install -r requirements.txt`
  - Configure `.env` with `GEMINI_API_KEY` and `YOUR_EMAIL`
- **Run:** `python app.py` (Flask server at `http://127.0.0.1:5001`)
- **Test API:** POST to `/recommend` with JSON body `{ "title": ..., "abstract": ... }`

## Patterns & Conventions
- **Keyword Extraction:** Always sanitize keywords (lowercase, remove special chars, min length 4)
- **Embeddings:** Use `SentenceTransformer('all-MiniLM-L6-v2')` (fail gracefully if unavailable)
- **External APIs:**
  - OpenAlex: Use `YOUR_EMAIL` for all requests; handle API errors with debug prints
  - Gemini: Load model/config at import; fail gracefully if missing
- **Data Contracts:** Use frozen dataclasses for all cross-service data
- **Error Handling:** Return informative JSON errors for all API failures
- **Debugging:** Print debug info for keyword extraction, API results, and model loading

## Integration Points
- **OpenAlex API:** Journal/author search, recent abstracts
- **Google Gemini:** Peer review question generation (RAG)
- **YAKE:** Local keyword extraction (no external calls)
- **SentenceTransformer:** Local semantic embeddings

## Examples
- See `app.py` for end-to-end API orchestration
- See `core/nlp_service.py` for keyword extraction and embedding patterns
- See `core/openalex_service.py` for external API integration and error handling
- See `core/rag_service.py` for LLM prompt engineering and Gemini usage

## Special Notes
- All service boundaries are Python modules in `core/`; keep business logic isolated
- Always use dataclasses for data passed between services
- Print debug info for all major steps (keyword extraction, API calls, model loading)
- Update `.env` for API keys/emails before running

---
**For unclear or missing conventions, ask the user for clarification or examples.**
