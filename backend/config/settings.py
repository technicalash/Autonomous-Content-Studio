from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Autonomous Content Studio"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///acs.db"
    
    GEMINI_API_KEY: str
    
    # Planner Defaults
    DEFAULT_PLATFORM: str = "Instagram"
    DEFAULT_LANGUAGE: str = "Hinglish"
    DEFAULT_GOAL: str = "Create a highly engaging and viral 'What If' short-form video."
    DEFAULT_AUDIENCE: str = "15-30 years"
    # Video Defaults
    DEFAULT_VIDEO_TYPE: str= "Short"
    DEFAULT_DURATION: int = 45
    # Planner Knowledge Paths 
    CATEGORIES_PATH: str = "backend/storage/knowledge/planner/categories.json"
    PLANNER_STYLE_PATH: str = "backend/storage/knowledge/planner/planner_style.txt"

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()