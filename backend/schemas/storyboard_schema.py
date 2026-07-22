from pydantic import BaseModel
from typing import List


class Scene(BaseModel):
    scene_number: int
    purpose: str
    narration: str
    duration_seconds: int


class StoryboardOutput(BaseModel):
    title: str
    hook: str
    scenes: List[Scene]
    ending: str
    call_to_action: str