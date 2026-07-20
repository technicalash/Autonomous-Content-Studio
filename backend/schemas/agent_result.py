from typing import Any, Optional

from pydantic import BaseModel


class AgentResult(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    next_stage: Optional[str] = None