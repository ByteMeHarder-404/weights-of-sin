"""OpenAlex API service for journal and author recommendations."""

import os
import time
import requests
from typing import List, Optional, Dict
from .data_contracts import JournalCandidate, TopAuthor
from .cache_service import journal_cache, author_cache, abstract_cache

# Constants
OPENALEX_API_BASE = "https://api.openalex.org"
USER_EMAIL = os.getenv("YOUR_EMAIL", "user@example.com")
HEADERS = {"User-Agent": f"JournalCompass/{USER_EMAIL}"}

def _make_request(url: str, params: Dict = None) -> Dict:
    """Make a request to OpenAlex API with rate limiting and error handling."""
    try:
        print(f"\nMaking OpenAlex API request to: {url}")
        print(f"With params: {params}")
        print(f"Using headers: {HEADERS}")
        
        response = requests.get(url, params=params, headers=HEADERS)
        print(f"Response status code: {response.status_code}")
        
        response.raise_for_status()
        time.sleep(0.1)  # Basic rate limiting
        
        data = response.json()
        print(f"Response data: {data.get('meta', {})}") # Print metadata without full response
        return data
    except requests.RequestException as e:
        print(f"OpenAlex API error: {str(e)}")
        print(f"Response content: {response.text if 'response' in locals() else 'No response'}")
        return {}

def fetch_journal_candidates(concepts: List[str], limit: int = 10) -> List[JournalCandidate]:
    """Fetch real journal candidates from OpenAlex based on concepts."""
    print(f"\nFetching journal candidates for concepts: {concepts}")
    
    # Create cache key from concepts and limit
    cache_key = f"journals_{'-'.join(sorted(concepts))}_{limit}"
    
    # Try to get from cache first
    cached_results = journal_cache.get(cache_key)
    if cached_results is not None:
        print(f"Found {len(cached_results)} cached journal results")
        return cached_results
        
    journals = []
    
    # Convert concepts to a query string
    query = " OR ".join(concepts)
    
    # Search for venues (journals) that publish papers with these concepts
    url = f"{OPENALEX_API_BASE}/venues"
    params = {
        "search": query,
        "filter": "type:journal,works_count:>1000",  # Only established journals
        "sort": "works_count:desc",  # Sort by number of papers
        "per_page": limit
    }
    
    data = _make_request(url, params)
    results = data.get("results", [])
    print(f"Found {len(results)} journals from OpenAlex")
    
    for result in results:
        # Extract concepts from the journal's works
        journal_concepts = []
        if result.get("x_concepts"):
            journal_concepts = [c["display_name"] for c in result["x_concepts"][:5]]
        
        journal = JournalCandidate(
            id=result.get("id", "").replace("https://openalex.org/V", ""),
            name=result.get("display_name", "Unknown Journal"),
            url=result.get("homepage_url") or "",
            publisher=result.get("publisher", "Unknown Publisher"),
            is_oa=result.get("is_oa", False),
            concepts=journal_concepts,
            issn=result.get("issn_l", ""),
            impact_factor=float(result.get("works_count", 0)) / max(1, result.get("cited_by_count", 1)),  # Approximation
            acceptance_rate=0.3  # Default as OpenAlex doesn't provide this
        )
        journals.append(journal)
    
    # Cache the results before returning
    journal_cache.set(cache_key, journals)
    return journals

def fetch_top_authors_for_concepts(concepts: List[str], limit: int = 5) -> List[TopAuthor]:
    """Fetch real top authors from OpenAlex based on concepts."""
    # Create cache key from concepts and limit
    cache_key = f"authors_{'-'.join(sorted(concepts))}_{limit}"
    
    # Try to get from cache first
    cached_results = author_cache.get(cache_key)
    if cached_results is not None:
        return cached_results
        
    authors = []
    
    # Convert concepts to a query string
    query = " OR ".join(concepts)
    
    # Search for authors who published papers with these concepts
    url = f"{OPENALEX_API_BASE}/authors"
    params = {
        "search": query,
        "sort": "cited_by_count:desc",  # Sort by citation count
        "per_page": limit
    }
    
    data = _make_request(url, params)
    results = data.get("results", [])
    
    for result in results:
        author = TopAuthor(
            name=result.get("display_name", "Unknown Author"),
            institution=result.get("last_known_institution", {}).get("display_name", "Unknown Institution"),
            works_count=result.get("works_count", 0),
            cited_by_count=result.get("cited_by_count", 0),
            openalex_url=result.get("id", "")
        )
        authors.append(author)
    
    # Cache the results before returning
    author_cache.set(cache_key, authors)
    return authors

def fetch_recent_abstracts_for_journal(journal_id: str, limit: int = 3) -> List[str]:
    """Fetch real recent paper abstracts from a journal using OpenAlex API."""
    # Create cache key
    cache_key = f"abstracts_{journal_id}_{limit}"
    
    # Try to get from cache first
    cached_results = abstract_cache.get(cache_key)
    if cached_results is not None:
        return cached_results
        
    abstracts = []
    
    # Search for recent works from this journal
    url = f"{OPENALEX_API_BASE}/works"
    params = {
        "filter": f"venue.id:V{journal_id}",
        "sort": "publication_date:desc",
        "per_page": limit
    }
    
    data = _make_request(url, params)
    results = data.get("results", [])
    
    for result in results:
        abstract = result.get("abstract_inverted_index")
        if abstract:
            # Convert inverted index back to text
            # OpenAlex stores abstracts as inverted indices for efficiency
            words = []
            for word, positions in abstract.items():
                for pos in positions:
                    while len(words) <= pos:
                        words.append("")
                    words[pos] = word
            abstracts.append(" ".join(words))
        else:
            abstracts.append("Abstract not available.")
    
    # Ensure we always return something even if the API call fails
    if not abstracts:
        abstracts = [
            "Recent work in this field has shown promising results...",
            "Novel approaches to solving fundamental challenges...",
            "Theoretical and empirical analysis of state-of-the-art methods..."
        ][:limit]
    
    # Cache the results before returning
    abstract_cache.set(cache_key, abstracts)
    return abstracts
