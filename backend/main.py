from fastapi import FastAPI
from backend.config.settings import settings
from backend.database.database import SessionLocal
from backend.orchestrator.orchestrator import Orchestrator
from backend.schemas.project_context import ProjectContext
from backend.schemas.generate_request import GenerateRequest
from fastapi import HTTPException

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

@app.get("/")
def root():
    return{
        "message": "Welcome to Autonomous Content Studio"
    }

@app.post("/generate")
def generate(request: GenerateRequest):
    
    db = SessionLocal()
    try:
        orchestrator = Orchestrator(db)
        result = orchestrator.run()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
            )
    finally:
        db.close()      