import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    # FastAPI Configuration
    fastapi_env: str = os.getenv("FASTAPI_ENV", "development")
    fastapi_debug: bool = os.getenv("FASTAPI_DEBUG", "True").lower() == "true"
    fastapi_host: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
    fastapi_port: int = int(os.getenv("FASTAPI_PORT", "8000"))

    # NewRelic Configuration
    new_relic_license_key: Optional[str] = os.getenv("NEW_RELIC_LICENSE_KEY")
    new_relic_app_name: str = os.getenv("NEW_RELIC_APP_NAME", "FastAPI Demo App")

    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # Application Configuration
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key")
    api_v1_prefix: str = os.getenv("API_V1_PREFIX", "/api/v1")
    project_name: str = os.getenv("PROJECT_NAME", "FastAPI NewRelic Demo")
    project_version: str = os.getenv("PROJECT_VERSION", "1.0.0")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
