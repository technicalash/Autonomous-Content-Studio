from pydantic import BaseModel
from typing import List


class ProjectPlan(BaseModel):
    topic: str
    category: str
    goal: str
    audience: str
    platform: str
    language: str
    video_type: str
    duration: int
    style: str
    hook_style: str
    research_points: List[str]
    reasoning: str