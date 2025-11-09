"""
Application configuration
Loaded from environment variables
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Application
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # Database
    DATABASE_URL: str = "postgresql://legally_ai:legally_ai_dev_password@postgres:5432/legally_ai"

    # Redis
    REDIS_URL: str = "redis://:legally_ai_redis_dev@redis:6379/0"

    # LLM Provider
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str | None = None
    DEFAULT_MODEL: str = "llama-3.3-70b-versatile"

    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "/app/uploads"

    # Languages
    SUPPORTED_LANGUAGES: str = "russian,serbian,french,english"

    # Stripe (optional)
    STRIPE_SECRET_KEY: str | None = None
    STRIPE_WEBHOOK_SECRET: str | None = None

    # Sentry (optional)
    SENTRY_DSN: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
