from pydantic import BaseModel
from typing import Optional


class ProjectContext(BaseModel):
    project_id: Optional[int] = None
    topic: Optional[str] = None
    category: Optional[str] = None
    platform: Optional[str] = None
    duration: Optional[int] = None
    language: Optional[str] = None
    status: Optional[str] = None