from abc import ABC, abstractmethod

from backend.schemas.project_context import ProjectContext
from backend.schemas.agent_result import AgentResult


class BaseAgent(ABC):

    @abstractmethod
    def execute(self, context: ProjectContext) -> AgentResult:
        """
        Execute the agent.
        """
        pass