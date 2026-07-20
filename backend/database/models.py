from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    category = Column(String)
    platform = Column(String)
    language = Column(String)
    status = Column(String)

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    goal = Column(String)
    audience = Column(String)
    style = Column(String)
    duration = Column(Integer)