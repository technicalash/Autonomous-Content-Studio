from backend.agents.base_agent import BaseAgent
from backend.schemas.project_context import ProjectContext
from backend.schemas.agent_result import AgentResult
from backend.services.memory_service import MemoryService


class PlannerAgent(BaseAgent):
    def __init__(self):
        self.memory_service = MemoryService()
    def execute(self, context: ProjectContext) -> AgentResult:

        plan = {
            "goal": "Create an engaging educational short",
            "audience": "General Audience",
            "style": "Cinematic",
            "duration": 45
        }
        self.memory_service.save_plan(
            context.project_id,
            plan
        )

        return AgentResult(
            success=True,
            message="Planning completed successfully.",
            data=plan,
            next_stage=None
        )