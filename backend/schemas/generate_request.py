from pydantic import BaseModel


class GenerateRequest(BaseModel):
    topic: str
    category: str
    platform: str
    duration: int
    language: str