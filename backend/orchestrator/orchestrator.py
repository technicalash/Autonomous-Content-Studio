from backend.schemas.project_context import ProjectContext
from backend.schemas.agent_result import AgentResult

from backend.agents.planner_agent import PlannerAgent
from backend.agents.research_agent import ResearchAgent
from backend.agents.storyboard_agent import StoryboardAgent
from backend.services.project_service import ProjectService


class Orchestrator:

    def __init__(self, db):
        self.db = db

        self.project_service = ProjectService()

        self.planner = PlannerAgent(db)
        self.research = ResearchAgent(db)
        self.storyboard=StoryboardAgent(db)

    def run(self) -> AgentResult:

        # Create an empty project
        project = self.project_service.create_project(self.db)

        # Planner generates the ProjectPlan
        result = self.planner.execute(project.id)
        
        if not result.success:
            self.project_service.update_status(
                self.db,
                project.id,
                "planning_failed"
            )
            return result
        
        self.project_service.update_project(
        self.db,
        project.id,
        result.data
        )
        
        research_result = self.research.execute(project.id)
        if not research_result.success:
            self.project_service.update_status(
                self.db,
                project.id,
                "research_failed"
            )
            return research_result
        
        # STORYBOARD AGENT 
        
        story_result=self.storyboard.execute(project.id)
        if not story_result.success:
            self.project_service.update_status(
                self.db,
                project.id,
                "research_failed"
            )
            return story_result 