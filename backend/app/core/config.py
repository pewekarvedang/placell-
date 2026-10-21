import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory of the backend repository
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "placell.db").replace("\\", "/")

class Settings(BaseSettings):
    PROJECT_NAME: str = "Placell"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "placell-super-secret-production-key-2026-final-year")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database: Supports PostgreSQL, defaults to local backend/placell.db
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{DEFAULT_DB_PATH}"
    )
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    model_config = SettingsConfigDict(case_sensitive=True, extra="ignore")

settings = Settings()
