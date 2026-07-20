from backend.schemas.project_context import ProjectContext
from backend.schemas.agent_result import AgentResult

from backend.agents.planner_agent import PlannerAgent
from backend.services.project_service import ProjectService


class Orchestrator:

    def __init__(self):
        self.project_service = ProjectService() 
        self.planner = PlannerAgent()

    def run(self, context: ProjectContext) -> AgentResult:
        project = self.project_service.create_project(
            topic=context.topic,
            category=context.category,
            platform=context.platform,
            language=context.language
        )
        context.project_id = project.id
        result = self.planner.execute(context)
        return result