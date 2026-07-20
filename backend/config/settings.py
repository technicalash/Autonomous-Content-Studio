from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Autonomous Content Studio"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///acs.db"

    class Config:
        env_file = ".env"


settings = Settings()