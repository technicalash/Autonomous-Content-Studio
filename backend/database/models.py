from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import JSON, Text

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=True)
    category = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    language = Column(String, nullable=True)
    status = Column(String, nullable=False)

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"))

    goal = Column(String)
    audience = Column(String)
    video_type = Column(String)
    style = Column(String)
    hook_style = Column(String)
    duration = Column(Integer)
    reasoning = Column(Text)
    research_points = Column(JSON)
    
# RESEARCH MODEL 

class Research(Base):

    __tablename__ = "research"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    topic = Column(String)

    summary = Column(Text)

    research_point_findings = Column(JSON)

    scientific_facts = Column(JSON)

    interesting_facts = Column(JSON)

    consequences = Column(JSON)

    misconceptions = Column(JSON)

    references = Column(JSON)

# STORYBOARD MODEL

class Storyboard(Base):
    __tablename__ = "storyboards"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False
    )

    title = Column(String)

    hook = Column(String)

    scenes = Column(JSON)

    ending = Column(String)

    call_to_action = Column(String)