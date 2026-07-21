from pydantic import BaseModel
from typing import List, Dict


class ResearchOutput(BaseModel):

    topic: str

    summary: str

    research_point_findings: Dict[str, str]

    scientific_facts: List[str]

    interesting_facts: List[str]

    consequences: List[str]

    misconceptions: List[str]

    references: List[str]