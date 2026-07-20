from fastapi import FastAPI
from backend.config.settings import settings
from backend.database import database
from backend.orchestrator.orchestrator import Orchestrator
from backend.schemas.project_context import ProjectContext
from backend.schemas.generate_request import GenerateRequest

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

    context = ProjectContext(
        topic=request.topic,
        category=request.category,
        platform=request.platform,
        duration=request.duration,
        language=request.language,
        status="planning"
    )

    orchestrator = Orchestrator()

    result = orchestrator.run(context)

    return result