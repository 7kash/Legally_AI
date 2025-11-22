"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .api import api_router
from .database import init_db

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multilingual contract analysis API",
    docs_url="/docs",
    redoc_url="/redoc",
    # Disable automatic trailing slash redirects to preserve CORS headers
    # Without this, FastAPI redirects /contracts to /contracts/ which loses CORS headers
    redirect_slashes=False
)

# Add CORS middleware
# Must be added before other middleware to handle CORS properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include API routers
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy"}
    )


@app.delete("/admin/clear-test-users")
def clear_test_users():
    """
    Admin endpoint to clear test users (development only)
    WARNING: This endpoint should be removed in production!
    """
    from .database import SessionLocal
    from .models.user import User

    db = SessionLocal()
    try:
        # Count test users
        test_users = db.query(User).filter(
            User.email.like('test%@example.com')
        ).all()

        emails = [u.email for u in test_users]

        # Delete them
        deleted = db.query(User).filter(
            User.email.like('test%@example.com')
        ).delete(synchronize_session=False)

        db.commit()

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "deleted": deleted,
                "emails": emails
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
