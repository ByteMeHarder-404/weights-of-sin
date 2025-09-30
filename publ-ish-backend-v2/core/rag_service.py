# filename: core/rag_service.py

import os
import json
import google.generativeai as genai
from .data_contracts import JournalCandidate
from typing import List

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: raise ValueError("GEMINI_API_KEY not found.")
    genai.configure(api_key=api_key)
    
    GENERATION_CONFIG = {"temperature": 0.4, "top_p": 1, "top_k": 1, "max_output_tokens": 1024}
    MODEL = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-09-2025", generation_config=GENERATION_CONFIG)
    print("RAG Service: Gemini model loaded.")
    
except Exception as e:
    MODEL = None
    print(f"CRITICAL RAG Service Error: {e}")

def generate_peer_review_questions(user_abstract: str, journal: JournalCandidate, recent_abstracts: List[str]) -> List[str]:
    if not MODEL:
        return ["RAG model is not configured or failed to load."]
    
    # Create a concise summary of recent papers to give the LLM context
    context_summary = "\n- ".join(recent_abstracts)

    prompt = f"""
You are a senior peer reviewer for a prestigious academic journal named "{journal.name}". You are known for your insightful and critical questions that push research forward.

A new paper has been submitted to your journal. Your task is to generate three critical and thoughtful questions for the author. These questions should be inspired by the journal's recent publications and its core focus.

**CONTEXT: RECENTLY PUBLISHED PAPER ABSTRACTS IN '{journal.name}'**
---
- {context_summary}
---

**NEW SUBMISSION ABSTRACT:**
---
{user_abstract}
---

**YOUR TASK:**
Based on the context of the journal's recent publications, review the new submission abstract. Generate exactly three probing questions a real reviewer would ask. Focus on methodology, novelty, contribution to the field, and potential limitations.

Provide your response as a strict JSON list of strings. Example: ["question 1", "question 2", "question 3"]

**JSON List of Questions Only:**
"""

    try:
        response = MODEL.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        questions = json.loads(cleaned_response)
        return questions if isinstance(questions, list) else [str(questions)]
    except Exception as e:
        print(f"RAG Generation Error for journal {journal.name}: {e}")
        return [
            "How does this work's methodology compare to established practices in the field?",
            "What is the primary novel contribution of this paper beyond incremental improvements?",
            "What are the potential limitations or boundary conditions of the proposed approach?"
        ]