# filename: core/openalex_service.py

import os
import requests
from typing import List
from .data_contracts import JournalCandidate, TopAuthor


YOUR_EMAIL_ADDRESS = os.getenv("YOUR_EMAIL", "anonymous@example.com")
if YOUR_EMAIL_ADDRESS == "your.email@example.com" or YOUR_EMAIL_ADDRESS == "anonymous@example.com":
    print("WARNING: YOUR_EMAIL is not set to a real address. Set it in your .env file for OpenAlex API access.")

def deinvert_abstract(inverted_abstract: dict) -> str:
    if not inverted_abstract: return ""
    try:
        index_to_word = {index: word for word, indices in inverted_abstract.items() for index in indices}
        if not index_to_word: return ""
        max_index = max(index_to_word.keys())
        return " ".join(index_to_word.get(i, "") for i in range(max_index + 1))
    except Exception: return ""

def fetch_journal_candidates(keywords: List[str], pool_size: int = 30) -> List[JournalCandidate]:
    if not keywords: return []
    
    # Filter keywords to only single words or short phrases (max 2 words)
    filtered_keywords = [kw for kw in keywords if len(kw.split()) <= 2]
    if not filtered_keywords:
        print(f"ERROR: No valid keywords for OpenAlex search after filtering. Original: {keywords}")
        return []
    # Use only the first valid keyword for OpenAlex search
    search_string = filtered_keywords[0]
    params = {
        'search': search_string, 'per-page': pool_size,
        'select': "id,display_name,homepage_url,host_organization_name,is_oa,x_concepts",
        'mailto': YOUR_EMAIL_ADDRESS
    }
    full_url = "https://api.openalex.org/journals"
    print(f"--- DEBUG: OpenAlex Journals Request URL: {full_url}")
    print(f"--- DEBUG: OpenAlex Journals Request Params: {params}")
    try:
        response = requests.get(full_url, params=params, timeout=10)
        print(f"--- DEBUG: OpenAlex Response Status Code: {response.status_code}")
        print(f"--- DEBUG: OpenAlex Response Text: {response.text[:500]}")
        response.raise_for_status()
        results = response.json().get('results', [])
        print(f"--- DEBUG: Found {len(results)} journal candidates for keywords: {keywords}")
    except requests.exceptions.RequestException as e:
        print(f"API Error (Journals): {e}")
        return []

    return [
        JournalCandidate(
            id=j.get('id'), name=j.get('display_name', 'N/A'),
            url=j.get('homepage_url', '#'), publisher=j.get('host_organization_name', 'N/A'),
            is_oa=j.get('is_oa', False),
            concepts=[c.get('display_name') for c in j.get('x_concepts', []) if c.get('display_name')][:5]
        ) for j in results
    ]

def fetch_top_authors_for_concepts(keywords: List[str], count: int = 5) -> List[TopAuthor]:
    if not keywords: return []

    # Filter keywords to only single words or short phrases (max 2 words)
    filtered_keywords = [kw for kw in keywords if len(kw.split()) <= 2]
    if not filtered_keywords:
        print(f"ERROR: No valid keywords for OpenAlex author search after filtering. Original: {keywords}")
        return []
    # Use only the first valid keyword for OpenAlex author search
    search_string = filtered_keywords[0]
    params = {
        'search': search_string, 'per-page': count, 'sort': 'cited_by_count:desc',
        'select': 'id,display_name,last_known_institution,works_count,cited_by_count',
        'mailto': YOUR_EMAIL_ADDRESS
    }
    try:
        response = requests.get("https://api.openalex.org/authors", params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get('results', [])
        print(f"--- DEBUG: Found {len(results)} top authors for keywords: {keywords}")
    except requests.exceptions.RequestException as e:
        print(f"API Error (Authors): {e}")
        return []

    return [
        TopAuthor(
            name=a.get('display_name', 'N/A'),
            institution=a.get('last_known_institution', {}).get('display_name', 'N/A') if a.get('last_known_institution') else 'N/A',
            works_count=a.get('works_count', 0), cited_by_count=a.get('cited_by_count', 0),
            openalex_url=a.get('id')
        ) for a in results
    ]

def fetch_recent_abstracts_for_journal(journal_id: str, count: int = 10) -> List[str]:
    if not journal_id: return []
    params = {
        'filter': f'primary_location.source.id:{journal_id}', 'per-page': count,
        'sort': 'publication_date:desc', 'select': 'abstract_inverted_index',
        'mailto': YOUR_EMAIL_ADDRESS
    }
    try:
        response = requests.get("https://api.openalex.org/works", params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"API Error (Abstracts): {e}")
        return []
    return [deinvert_abstract(work.get('abstract_inverted_index')) for work in results]