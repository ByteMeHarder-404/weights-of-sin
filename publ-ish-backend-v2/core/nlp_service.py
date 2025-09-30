# filename: core/nlp_service.py

import yake
from sentence_transformers import SentenceTransformer
import re

# --- MODEL LOADING ---
print("Loading NLP models...")
try:
    EMBEDDING_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    print("Semantic model (sentence-transformer) loaded successfully.")
except Exception as e:
    EMBEDDING_MODEL = None
    print(f"CRITICAL ERROR: Could not load sentence-transformer model. {e}")

# This configuration is set to find meaningful 2 or 3-word phrases.
CONCEPT_EXTRACTOR = yake.KeywordExtractor(lan="en", n=3, dedupLim=0.9, top=7, features=None)
print("Keyword extractor (YAKE) initialized.")
# --- END MODEL LOADING ---


def extract_keywords_from_text(text: str) -> list:
    """
    Uses the local YAKE model to extract and sanitize keywords from text.
    This is the most robust method as it has no external dependencies.
    """
    if not text.strip(): return []

    keywords_with_scores = CONCEPT_EXTRACTOR.extract_keywords(text)
    
    sanitized_keywords = []
    for kw, score in keywords_with_scores:
        # Sanitize the keyword: lowercase, remove special characters, keep spaces.
        # This is crucial to prevent "Bad Request" errors from the API.
        sanitized_kw = re.sub(r'[^a-zA-Z0-9\s]', '', kw).lower()
        
        # Filter out keywords that are too short or just numbers after sanitization
        if len(sanitized_kw.strip()) > 3 and not sanitized_kw.strip().isdigit():
            sanitized_keywords.append(sanitized_kw.strip())
            
    # Return a simple list of the best, cleaned keywords
    return sanitized_keywords[:5] # Return the top 5 valid keywords

def get_semantic_embeddings(texts: list) -> list:
    """Generates semantic vector embeddings for a list of texts."""
    if not EMBEDDING_MODEL:
        print("Error: Embedding model is not available.")
        return [[] for _ in texts]
    
    return EMBEDDING_MODEL.encode(texts, convert_to_tensor=False)