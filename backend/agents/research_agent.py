from backend.agents.base_agent import BaseAgent
from backend.schemas.agent_result import AgentResult
from backend.services.memory_service import MemoryService
from backend.config.settings import settings
import json
from agno.agent import Agent
from agno.models.google import Gemini
from backend.schemas.research_schema import ResearchOutput
from backend.services.project_service import ProjectService
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.wikipedia import WikipediaTools


class ResearchAgent(BaseAgent):

    def __init__(self, db):
        super().__init__()

        self.db = db

        self.memory_service = MemoryService()
        self.project_service = ProjectService()

        self.agent = Agent(
            model=Gemini(
                id="gemini-2.5-flash",
                api_key=settings.GEMINI_API_KEY
            ),
            output_schema=ResearchOutput
        )
        
    def _build_prompt(self, project, plan):
        return f"""
You are the Research Agent of an Autonomous AI Content Studio.

Your responsibility is to perform accurate research and produce structured knowledge that will later be used by the Storyboard Agent.

=========================
PROJECT
=========================

Topic:
{project.topic}

Category:
{project.category}

Audience:
{plan.audience}

Language:
{project.language}

Duration:
{plan.duration}

Style:
{plan.style}

=========================
RESEARCH OBJECTIVES
=========================

Research the following topics:

{json.dumps(plan.research_points, indent=2)}

=========================
OUTPUT REQUIREMENTS
=========================

Generate a valid ResearchOutput object with the following fields.

1. topic
- Copy the project topic exactly.

2. summary
- Write a concise overview of the topic (100–150 words).
- Make it informative and engaging.

3. research_point_findings
- Create one dictionary entry for EVERY research point.
- The key MUST exactly match the research point.
- The value should contain a concise explanation.

Example:

Research Points:

[
    "Scientific Basis",
    "Possible Consequences",
    "Current Technology"
]

Output:

{{
    "Scientific Basis": "...",
    "Possible Consequences": "...",
    "Current Technology": "..."
}}

Never use placeholder keys like "example_key".

4. scientific_facts
- Return 5-8 scientifically accurate facts.
- Each fact must be a separate list item.
- Only include verified information.

5. interesting_facts
- Return 5-8 curiosity-generating facts.
- Make them suitable for short-form educational content.
- Use natural Hinglish when appropriate.

6. consequences
- Return 4-8 important consequences of this scenario.
- Each consequence should be a separate list item.

Example:

[
    "Humans may achieve digital immortality.",
    "Identity laws would need to change.",
    "Cybersecurity risks would become much more dangerous.",
    "Social inequality could increase."
]

7. misconceptions
- Return 3-5 common misconceptions.
- Briefly explain why each one is incorrect.

Example:

[
    "Uploading memories is the same as uploading consciousness.",
    "Mind uploading guarantees immortality.",
    "Current AI can already copy a human brain."
]

8. references
- Return reliable sources such as:
    - NASA
    - ESA
    - Nature
    - Science
    - Stanford Encyclopedia of Philosophy
    - Oxford University
    - Peer-reviewed journals

Only include trustworthy references.

=========================
RULES
=========================

1. Be scientifically accurate.
2. Prioritize factual correctness over creativity.
3. Keep explanations concise and easy to understand.
4. Do NOT generate a script.
5. Do NOT generate narration.
6. Do NOT generate scene descriptions.
7. Do NOT generate image prompts.
8. Do NOT include markdown.
9. Do NOT include placeholder values such as "example_key".
10. Return ONLY a valid ResearchOutput object that matches the schema.
"""
    def execute(self, project_id):
        try:
            plan = self.memory_service.get_plan(
                self.db,
                project_id
            )
            project = self.project_service.get_project(
                self.db,
                project_id
                )
            print("plan -------> ",plan)
            print("project -------> ",project)
            prompt = self._build_prompt(project, plan)
            response = self.agent.run(prompt)

            research = response.content
            print("research -------> ",research)

            self.memory_service.save_research(
                self.db,
                project_id,
                research
            )
            
            return AgentResult(
                success=True,
                message="Research completed successfully.",
                data=research,
                next_stage=None
            )

        except Exception as e:

            raise Exception(f"Research Agent Failed: {e}")
        
