import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "VisWeb"
    DESCRIPTION: str = "Personal data tracking API for health metrics and exercise"
    VERSION: str = "0.1.0"
    
    # CORS configuration
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database settings
    DATABASE_URL: Optional[str] = None
    
    # Grafana settings
    GRAFANA_URL: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

# If DATABASE_URL not explicitly set, use SQLite
if not settings.DATABASE_URL:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    DB_PATH = os.path.join(DATA_DIR, "visweb.db")
    settings.DATABASE_URL = f"sqlite:///{DB_PATH}"
