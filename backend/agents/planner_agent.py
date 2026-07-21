from backend.agents.base_agent import BaseAgent
from backend.schemas.project_context import ProjectContext
from backend.schemas.agent_result import AgentResult
from backend.services.memory_service import MemoryService
from backend.config.settings import settings
import json
from agno.agent import Agent
from agno.models.google import Gemini
from backend.schemas.project_plan import ProjectPlan


class PlannerAgent(BaseAgent):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.memory_service = MemoryService()
        self.agent = Agent(
            model=Gemini(
                id="gemini-2.5-flash",
                api_key=settings.GEMINI_API_KEY
                ),
            output_schema=ProjectPlan
            )
    
    def _load_settings(self):
        return {
            "platform": settings.DEFAULT_PLATFORM,
            "language": settings.DEFAULT_LANGUAGE,
            "goal": settings.DEFAULT_GOAL,
            "audience": settings.DEFAULT_AUDIENCE,
            "video_type": settings.DEFAULT_VIDEO_TYPE,
            "duration": settings.DEFAULT_DURATION
            }
        
    def _load_categories(self):
        with open(settings.CATEGORIES_PATH, "r") as file:
            return json.load(file)
        
    def _load_planner_style(self):
        with open(settings.PLANNER_STYLE_PATH, "r") as file:
            return file.read()
    def _load_recent_projects(self):
        return self.memory_service.get_recent_projects(
            self.db
            )
    def _load_top_projects(self):
        return self.memory_service.get_top_projects(
            self.db
            )
    def _build_context(self):
        return {
            "settings": self._load_settings(),
            "categories": self._load_categories(),
            "planner_style": self._load_planner_style(),
            "previous_projects": self._load_recent_projects(),
            "top_performing_projects": self._load_top_projects()
            }
    
    def _build_prompt(self, context):
        return f"""
You are the Planner Agent of an Autonomous AI Content Studio.

Your responsibility is to generate ONE unique, engaging, and high-quality ProjectPlan for the next social media video.

=========================
CONTENT NICHE
=========================

The content focuses on imaginative, entertaining, creative, and educational hypothetical scenarios designed to spark curiosity and encourage viewers to think.

The videos should belong to one of these content formats:

- What If...
- How Would...
- Imagine If...
- Could Humanity...
- What Happens If...
- Why Doesn't...

Examples include:
- What if Earth had two moons?
- What if dinosaurs never went extinct?
- How would humans survive on Mars?
- Imagine if gravity suddenly became half as strong.
- Could humanity survive without electricity?
- What happens if the Sun disappeared for one day?
- Why doesn't the Moon have an atmosphere?

The generated topic should:
- Be scientifically interesting, historically interesting, technologically interesting, or creatively speculative.
- Be suitable for a short-form social media video.
- Immediately spark curiosity.
- Encourage viewers to watch until the end.
- Be original and avoid overused ideas.
- Have the potential to become viral.

=========================
OBJECTIVE
=========================

Generate a complete ProjectPlan for ONE new video.

=========================
DEFAULT SETTINGS
=========================

{json.dumps(context["settings"], indent=2)}

=========================
AVAILABLE CATEGORIES
=========================

{json.dumps(context["categories"], indent=2)}

Category Selection Strategy

Select the category intelligently by balancing content diversity and historical performance.

Follow these rules:

1. Ensure that every available category gets an opportunity to appear regularly.
2. Analyze the categories used in the recent projects.
3. If one or more categories have not appeared in the recent videos, prioritize those categories.
4. If all categories have already appeared recently, you may choose the category that has historically performed the best.
5. Avoid repeating the same category in consecutive videos unless there is a strong reason based on previous performance.
6. Your final category should maximize both variety and long-term audience engagement.

=========================
PLANNER STYLE
=========================

{context["planner_style"]}

=========================
RECENT PROJECTS
=========================

{json.dumps(context["previous_projects"], indent=2)}

Use these recent projects to:
- avoid repeating topics,
- understand recent category usage,
- maintain content variety.

=========================
TOP PERFORMING PROJECTS
=========================

{json.dumps(context["top_performing_projects"], indent=2)}

Analyze why these projects performed well.
Learn from their patterns, but DO NOT copy or make only minor modifications to existing ideas.

=========================
RULES
=========================

1. Generate exactly ONE ProjectPlan.
2. The topic must be original, engaging, and curiosity-driven.
3. Do not repeat or closely resemble previous topics.
4. Select the category by following the Category Selection Strategy before generating the topic.
5. Create a powerful hook that encourages viewers to continue watching.
6. Generate research points that will help the Research Agent gather accurate and useful information.
7. Keep the reasoning concise.
8. Think like an experienced viral content strategist, not just an AI assistant.
9. Prioritize originality while learning from successful past content.
10. Learn from successful content patterns but maintain category diversity whenever possible.
11. Return ONLY a valid ProjectPlan that strictly follows the provided schema.
"""
    
    def _call_llm(self, prompt):
        response = self.agent.run(prompt)
        return response
    
    def _process_response(self, response):
        return response.content
    
    def execute(self, project_id: int) -> AgentResult:
        try:
            planner_context = self._build_context()
            prompt = self._build_prompt(planner_context)
            response = self._call_llm(prompt)
            plan = self._process_response(response)
            print("plan ----------> ",plan)
            self.memory_service.save_plan(
                self.db,
                project_id,
                plan
            )

            return AgentResult(
                success=True,
                message="Project plan generated successfully.",
                data=plan,
                next_stage="Research Agent"
            )
        except Exception as e:
            return AgentResult(
                success=False,
                message=f"Planner failed: {str(e)}",
                data=None,
                next_stage=None
            )