from backend.database.database import SessionLocal
from backend.database.models import Project


class ProjectService:

    def create_project(
        self,
        topic: str,
        category: str,
        platform: str,
        language: str
    ) -> Project:

        db = SessionLocal()

        project = Project(
            topic=topic,
            category=category,
            platform=platform,
            language=language,
            status="planning"
        )

        db.add(project)
        db.commit()
        db.refresh(project)
        db.close()

        return project