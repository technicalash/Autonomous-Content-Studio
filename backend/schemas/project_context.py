from pydantic import BaseModel
from typing import Optional


class ProjectContext(BaseModel):
    project_id: Optional[int] = None
    topic: str
    category: str
    platform: str
    duration: int
    language: str
    status: str