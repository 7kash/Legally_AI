"""
Legally AI - FastAPI Application
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

from .config import settings

# Initialize Sentry if DSN provided
if settings.SENTRY_DSN:
    try:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[FastApiIntegration()],
            traces_sample_rate=0.1,
            environment="production" if not settings.DEBUG else "development"
        )
    except Exception as e:
        # If Sentry DSN is invalid or not configured properly, just skip it
        print(f"Warning: Failed to initialize Sentry: {e}")
        print("Continuing without error tracking...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered multilingual contract analysis",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Health check
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app": settings.APP_NAME
    }


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Legally AI API",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else None
    }


# Import and include routers
from .api import auth, contracts, analyses, account

app.include_router(auth.router, prefix=f"{settings.API_PREFIX}/auth", tags=["auth"])
app.include_router(contracts.router, prefix=f"{settings.API_PREFIX}/contracts", tags=["contracts"])
app.include_router(analyses.router, prefix=f"{settings.API_PREFIX}/analyses", tags=["analyses"])
app.include_router(account.router, prefix=f"{settings.API_PREFIX}/account", tags=["account"])

# TODO: Add more routers as they're created
# from .api import deadlines, billing
# app.include_router(deadlines.router, prefix=f"{settings.API_PREFIX}/deadlines", tags=["deadlines"])
# app.include_router(billing.router, prefix=f"{settings.API_PREFIX}/billing", tags=["billing"])


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"LLM Provider: {settings.LLM_PROVIDER}")

    # TODO: Initialize database connection pool
    # TODO: Initialize Redis connection
    # TODO: Verify LLM API keys


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    print(f"Shutting down {settings.APP_NAME}")

    # TODO: Close database connections
    # TODO: Close Redis connections
