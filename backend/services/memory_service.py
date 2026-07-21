from backend.database.database import SessionLocal
from backend.database.models import Plan
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

    def save_research(self, project_id, research):
        pass

    def get_research(self, project_id):
        pass

    def save_storyboard(self, project_id, storyboard):
        pass

    def get_storyboard(self, project_id):
        pass