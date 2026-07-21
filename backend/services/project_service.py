from backend.database.database import SessionLocal
from backend.database.models import Project


class ProjectService:

    def create_project(self, db) -> Project:

        project = Project(
            status="planning"
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        return project
    
    def update_project(self, db, project_id, plan):
        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
            )
        project.topic = plan.topic
        project.category = plan.category
        project.platform = plan.platform
        project.language = plan.language
        project.status = "research"

        db.commit()

        return project
    def update_status(self, db, project_id, status):
        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )
        if project is None:
            return None
        project.status = status
        db.commit()
        db.refresh(project)
        return project