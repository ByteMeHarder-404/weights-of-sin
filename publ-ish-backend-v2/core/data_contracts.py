# filename: core/data_contracts.py

from dataclasses import dataclass, field, asdict
from typing import List

@dataclass(frozen=True)
class TopAuthor:
    name: str
    institution: str
    works_count: int
    cited_by_count: int
    openalex_url: str
    
    def to_dict(self):
        return asdict(self)

@dataclass(frozen=True)
class JournalCandidate:
    id: str
    name: str
    url: str
    publisher: str
    is_oa: bool
    concepts: List[str] = field(default_factory=list)
    issn: str = "0000-0000"
    impact_factor: float = 0.0
    acceptance_rate: float = 0.0
