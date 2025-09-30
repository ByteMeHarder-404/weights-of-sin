"""OpenAlex API service for journal and author recommendations."""

import os
import requests
from typing import List, Optional
from .data_contracts import JournalCandidate, TopAuthor

def fetch_journal_candidates(concepts: List[str]) -> List[JournalCandidate]:
    """Mock function to return journal candidates based on concepts."""
    return [
        JournalCandidate(
            id="J175083",
            name="Nature Machine Intelligence",
            url="https://www.nature.com/natmachintell/",
            publisher="Nature Portfolio",
            is_oa=False,
            concepts=["artificial intelligence", "machine learning", "computer science"],
            issn="2522-5839",
            impact_factor=15.508,
            acceptance_rate=0.15
        ),
        JournalCandidate(
            id="J91304",
            name="IEEE Transactions on Pattern Analysis and Machine Intelligence",
            url="https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=34",
            publisher="IEEE",
            is_oa=False,
            concepts=["artificial intelligence", "computer vision", "pattern recognition"],
            issn="0162-8828",
            impact_factor=24.314,
            acceptance_rate=0.25
        ),
        JournalCandidate(
            id="J15321",
            name="Journal of Machine Learning Research",
            url="https://jmlr.org/",
            publisher="JMLR",
            is_oa=True,
            concepts=["machine learning", "statistical learning", "computational learning theory"],
            issn="1533-7928",
            impact_factor=5.713,
            acceptance_rate=0.22
        )
    ]

def fetch_top_authors_for_concepts(concepts: List[str]) -> List[TopAuthor]:
    """Mock function to return top authors in the given concept areas."""
    return [
        TopAuthor(
            name="Geoffrey Hinton",
            institution="University of Toronto & Google Brain",
            works_count=200,
            cited_by_count=500000,
            openalex_url="https://openalex.org/authors/A1234567"
        ),
        TopAuthor(
            name="Yann LeCun",
            institution="New York University & Meta AI Research",
            works_count=180,
            cited_by_count=450000,
            openalex_url="https://openalex.org/authors/A2345678"
        ),
        TopAuthor(
            name="Yoshua Bengio",
            institution="University of Montreal & Mila",
            works_count=190,
            cited_by_count=400000,
            openalex_url="https://openalex.org/authors/A3456789"
        )
    ]

def fetch_recent_abstracts_for_journal(journal_id: str) -> List[str]:
    """Mock function to return recent paper abstracts from a journal."""
    abstracts = {
        "J175083": [  # Nature Machine Intelligence
            "We present a novel deep learning architecture for quantum state reconstruction...",
            "A breakthrough in self-supervised learning enables robots to learn from raw sensory input...",
            "New theoretical bounds on the sample complexity of reinforcement learning algorithms..."
        ],
        "J91304": [  # TPAMI
            "Advanced techniques for 3D scene understanding using multi-modal sensor fusion...",
            "Robust object detection in adverse weather conditions using radar and LiDAR...",
            "Novel attention mechanisms for fine-grained visual recognition tasks..."
        ],
        "J15321": [  # JMLR
            "Statistical analysis of deep neural networks reveals key factors in generalization...",
            "A unified framework for understanding optimization landscapes in deep learning...",
            "New theoretical insights into the role of network width in deep learning..."
        ]
    }
    return abstracts.get(journal_id, [
        "Recent work in this field has shown promising results...",
        "Novel approaches to solving fundamental challenges...",
        "Theoretical and empirical analysis of state-of-the-art methods..."
    ])
