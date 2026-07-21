from backend.database.database import SessionLocal
from backend.database.models import Plan, Research
from backend.database.models import Project

class MemoryService:

    def save_plan(self, db, project_id, plan):
        db_plan = Plan(
            project_id=project_id,
            goal=plan.goal,
            audience=plan.audience,
            video_type=plan.video_type,
            style=plan.style,
            hook_style=plan.hook_style,
            duration=plan.duration,
            reasoning=plan.reasoning,
            research_points=plan.research_points
            )
        db.add(db_plan)

        db.commit()

    def get_plan(self, db, project_id):
            plan = (
                db.query(Plan)
                .filter(Plan.project_id == project_id)
                .first()
                )
            return plan
    def get_recent_projects(self, db, limit=5):
        projects = (
            db.query(Project)
            .order_by(Project.id.desc())
            .limit(limit)
            .all()
            )
        return [
            {
                "topic": project.topic,
                "category": project.category
                }
            for project in projects
            ]
    def get_top_projects(self, db, limit=3):
        return []

    def save_research(self, db, project_id, research):
        research_db = Research(

            project_id=project_id,

            topic=research.topic,

            summary=research.summary,

            research_point_findings=research.research_point_findings,

            scientific_facts=research.scientific_facts,

            interesting_facts=research.interesting_facts,

            consequences=research.consequences,

            misconceptions=research.misconceptions,

            references=research.references
        )
        
        db.add(research_db)

        db.commit()

        db.refresh(research_db)

        return research_db

    def get_research(self, db, project_id):
        return (
        db.query(Research)
        .filter(
            Research.project_id == project_id
        )
        .first()
    )

    def save_storyboard(self, project_id, storyboard):
        pass

    def get_storyboard(self, project_id):
        pass