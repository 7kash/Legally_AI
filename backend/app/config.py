"""
Application configuration using environment variables.
"""

import os
from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

# Load .env file at module import time
# This ensures environment variables are available to os.getenv() calls
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    # App
    APP_NAME: str = "Legally AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/legally_ai"
    )
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", 10))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", 20))

    # Redis
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    # Celery
    CELERY_BROKER_URL: str = os.getenv(
        "CELERY_BROKER_URL",
        "redis://localhost:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.getenv(
        "CELERY_RESULT_BACKEND",
        "redis://localhost:6379/0"
    )

    # LLM APIs
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openrouter")
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "120"))  # Timeout in seconds
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-70b-instruct")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")  # Optional, if needed
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")

    # File Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/app/uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))  # 10MB
    MAX_FILE_SIZE_MB: int = 10  # Maximum file size in MB
    ALLOWED_EXTENSIONS: list = Field(default_factory=lambda: [".pdf", ".docx"])  # Allowed file extensions

    # CORS
    CORS_ORIGINS: list = Field(default_factory=lambda: [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://legally-ai.vercel.app"
    ])

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


settings = Settings()
