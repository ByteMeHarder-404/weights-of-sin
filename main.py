# PowerShell users: To run this FastAPI server, use the following command:
# & "C:/Users/Bhavik Sheth/AppData/Local/Programs/Python/Python313/python.exe" -m uvicorn main:app --reload
# This ensures the path with spaces is handled correctly.
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GEMINI_API_KEY = "AIzaSyA5RQc_cF2AmK_3T1eT7oUYjBwADw-Aees"
GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
OPENALEX_BASE_URL = "https://api.openalex.org"

class InputData(BaseModel):
    title: str
    abstract: str

@app.post("/search")
async def search_papers(data: InputData):
    # Step 1: Use Gemini to generate keywords or queries
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    prompt = f"Given the following title and abstract, generate a list of keywords for academic search. Title: {data.title} Abstract: {data.abstract}"
    gemini_payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    gemini_response = requests.post(gemini_url, json=gemini_payload)
    if gemini_response.status_code != 200:
        return {"error": "Gemini API error", "details": gemini_response.text}
    gemini_data = gemini_response.json()
    # Extract keywords from Gemini response
    try:
        keywords = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return {"error": "Failed to extract keywords from Gemini response", "details": gemini_data}
    # Step 2: Use OpenAlex to search for papers
    openalex_url = f"{OPENALEX_BASE_URL}/works"
    params = {
        "search": keywords,
        "per-page": 5
    }
    openalex_response = requests.get(openalex_url, params=params)
    if openalex_response.status_code != 200:
        return {"error": "OpenAlex API error", "details": openalex_response.text}
    openalex_data = openalex_response.json()
    # Step 3: Extract top papers and journals
    results = []
    for work in openalex_data.get("results", []):
        results.append({
            "title": work.get("title"),
            "journal": work.get("host_venue", {}).get("display_name"),
            "authors": [a.get("author", {}).get("display_name") for a in work.get("authorships", [])],
            "doi": work.get("doi"),
            "url": work.get("id")
        })
    return {"keywords": keywords, "papers": results}
