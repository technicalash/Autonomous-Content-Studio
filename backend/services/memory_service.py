from backend.database.database import SessionLocal
from backend.database.models import Plan

class MemoryService:

    def save_plan(self, project_id, plan):
        db = SessionLocal()

        db_plan = Plan(
            project_id=project_id,
            goal=plan["goal"],
            audience=plan["audience"],
            style=plan["style"],
            duration=plan["duration"]
        )
        db.add(db_plan)

        db.commit()

        db.close()

    def get_plan(self, project_id):
            db = SessionLocal()
            plan = (
                db.query(Plan)
                .filter(Plan.project_id == project_id)
                .first()
                )
            db.close()
            return plan

    def save_research(self, project_id, research):
        pass

    def get_research(self, project_id):
        pass

    def save_storyboard(self, project_id, storyboard):
        pass

    def get_storyboard(self, project_id):
        pass