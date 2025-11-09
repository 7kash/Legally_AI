"""
Application Configuration
Settings loaded from environment variables
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings from environment variables
    """

    # Application
    APP_NAME: str = "Legally AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days

    # LLM Providers
    LLM_PROVIDER: str = "groq"  # "groq" or "deepseek"
    GROQ_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None  # Fallback

    # File Storage
    UPLOAD_DIR: str = "/data/contracts"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: list[str] = [".pdf", ".docx"]

    # Trial Limits
    FREE_TIER_ANALYSES: int = 3

    # Stripe
    STRIPE_API_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_PRICE_ID_MONTHLY: Optional[str] = None
    STRIPE_PRICE_ID_ANNUAL: Optional[str] = None

    # SendGrid
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@legally-ai.com"

    # Frontend URL (for email links)
    FRONTEND_URL: str = "http://localhost:3000"

    # Sentry
    SENTRY_DSN: Optional[str] = None

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:7860",
        "https://legally-ai.vercel.app"
    ]

    # Celery
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Global settings instance
settings = Settings()
