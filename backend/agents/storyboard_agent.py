from backend.agents.base_agent import BaseAgent
from backend.schemas.agent_result import AgentResult
from backend.services.memory_service import MemoryService
from backend.config.settings import settings
import json
from agno.agent import Agent
from agno.models.google import Gemini
from backend.schemas.storyboard_schema import StoryboardOutput
from backend.services.project_service import ProjectService
from backend.database.database import SessionLocal

class StoryboardAgent(BaseAgent):

    def __init__(self, db):
        
        self.db = db
        self.memory_service = MemoryService()
        self.project_service = ProjectService()

        self.agent = Agent(
            model=Gemini(
                id="gemini-2.5-flash",
                api_key=settings.GEMINI_API_KEY
            ),
            output_schema=StoryboardOutput
        )
    def _build_prompt(self, project, plan, research):
        return f"""
You are the Storyboard Agent of an Autonomous AI Content Studio.

Your responsibility is to transform structured research into a highly engaging short-form video storyboard.

This storyboard will later be used by other AI agents to generate visuals, voice-over, and the final video.

=========================
PROJECT DETAILS
=========================

Topic:
{project.topic}

Category:
{project.category}

Platform:
{project.platform}

Language:
{project.language}

=========================
CONTENT STRATEGY
=========================

Goal:
{plan.goal}

Target Audience:
{plan.audience}

Video Type:
{plan.video_type}

Style:
{plan.style}

Hook Style:
{plan.hook_style}

Target Duration:
{plan.duration}

=========================
RESEARCH
=========================

Summary:
{research.summary}

Research Point Findings:
{json.dumps(research.research_point_findings, indent=2)}

Scientific Facts:
{json.dumps(research.scientific_facts, indent=2)}

Interesting Facts:
{json.dumps(research.interesting_facts, indent=2)}

Consequences:
{json.dumps(research.consequences, indent=2)}

Misconceptions:
{json.dumps(research.misconceptions, indent=2)}

=========================
YOUR TASK
=========================

Using ONLY the research provided above, create a compelling storyboard suitable for a short-form social media video.

The storyboard should:

• Immediately capture attention.
• Build curiosity throughout the video.
• Explain the topic using storytelling.
• Naturally include the provided scientific facts.
• Keep viewers engaged until the end.
• End with a memorable thought.
• Finish with a natural Call-To-Action.

=========================
STORY STRUCTURE
=========================

Generate EXACTLY the following:

1. One video title.

2. One hook.

3. EXACTLY 6 scenes.

4. One ending.

5. One call-to-action.

Do NOT generate more than 6 scenes.

=========================
SCENE STRUCTURE
=========================

Each scene MUST contain:

- Scene Number
- Narration
- Duration (seconds)

Narration Guidelines:

- 15-30 words per scene.
- Every scene must introduce NEW information.
- Never repeat previous narration.
- Never repeat scientific facts unless absolutely necessary.
- Each scene should smoothly transition to the next.
- Use a conversational tone.
- Sound like a viral YouTube Shorts narrator.
- Do NOT sound like an encyclopedia.
- Build suspense and curiosity.

Suggested Story Flow:

Scene 1:
Hook and introduce the concept.

Scene 2:
Explain the concept.

Scene 3:
Present scientific evidence or facts.

Scene 4:
Present interesting facts or possibilities.

Scene 5:
Discuss consequences or misconceptions.

Scene 6:
End with a thought-provoking conclusion.

=========================
DURATION
=========================

The combined narration of all scenes should approximately match the requested duration.

Do not make scenes unnecessarily long.

=========================
RULES
=========================

1. Use ONLY the provided research.
2. Do NOT invent scientific facts.
3. Do NOT repeat sentences.
4. Do NOT repeat scene ideas.
5. Do NOT duplicate scenes.
6. Every scene must contain unique information.
7. Do NOT generate image prompts.
8. Do NOT generate camera angles.
9. Do NOT generate editing instructions.
10. Do NOT use markdown.
11. Stop immediately after Scene 6, Ending, and Call-To-Action.
12. Return ONLY a valid StoryboardOutput object.
"""
    
    def execute(self, project_id):
        try:
            project = self.project_service.get_project(
                self.db,
                project_id
                )
            plan = self.memory_service.get_plan(
                self.db,
                project_id
                )
            research = self.memory_service.get_research(
                self.db,
                project_id
                )
            prompt = self._build_prompt(project, plan, research)
            storyboard = self.agent.run(prompt).content
            print("storyboard -------> ",storyboard)
            self.memory_service.save_storyboard(self.db, project_id, storyboard)
            return AgentResult(
                success=True,
                message="Storyboard generated successfully.",
                data=storyboard,
                next_stage=None
                )
        except Exception as e:
            return AgentResult(
                success=False,
                message=str(e),
                data=None,
                next_stage=None
                )