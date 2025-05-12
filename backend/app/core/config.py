from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator, Field
import json
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Backend"
    ENV: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api"
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "AAI_Project"
    
    # JWT
    SECRET_KEY: str = "your-super-secret-key-for-development-only"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # Auth settings
    USE_COOKIE_AUTH: bool = Field(default=False, env="USE_COOKIE_AUTH")
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
        
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # options: json, console
    LOG_FILE_PATH: Optional[Path] = None
    ENABLE_FILE_LOGGING: bool = False
    ENABLE_CONSOLE_LOGGING: bool = True
    
    # Elastic APM
    ELASTIC_APM_ENABLED: bool = False
    ELASTIC_APM_SERVER_URL: Optional[str] = None
    ELASTIC_APM_SERVICE_NAME: Optional[str] = None
    ELASTIC_APM_ENVIRONMENT: Optional[str] = None
    
    #CRON Configs
    EVALUATE_SOLUTION_CRON: str = "*/1 * * * *"
    EVALUATE_SOLUTIONS_BATCH_SIZE: int = 2
    EVALUATE_SOLUTIONS_DELAY_BETWEEN_ATTEMPTS: int = 2

    EVALUATE_INTERVIEW_CRON: str = "*/1 * * * *"
    EVALUATE_INTERVIEWS_BATCH_SIZE: int = 2
    EVALUATE_INTERVIEWS_DELAY_BETWEEN_ATTEMPTS: int = 2
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v
    
    @validator("LOG_FILE_PATH", pre=True)
    def validate_log_path(cls, v, values):
        if values.get("ENABLE_FILE_LOGGING", False):
            if not v:
                raise ValueError("LOG_FILE_PATH must be set when ENABLE_FILE_LOGGING is True")
            path = Path(v)
            path.parent.mkdir(parents=True, exist_ok=True)
            return path
        return v
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
