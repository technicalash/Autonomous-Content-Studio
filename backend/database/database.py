from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config.settings import settings
from backend.database.models import Base


DATABASE_URL=settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)