"""
Legally AI - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from contextlib import asynccontextmanager

# Version
VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"Starting Legally AI v{VERSION}")
    print(f"Debug mode: {os.getenv('DEBUG', 'False')}")
    print(f"LLM Provider: {os.getenv('LLM_PROVIDER', 'groq')}")

    yield

    # Shutdown
    print("Shutting down Legally AI")


# Create FastAPI app
app = FastAPI(
    title="Legally AI API",
    description="Multilingual contract analysis platform",
    version=VERSION,
    lifespan=lifespan,
)

# CORS middleware
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for Docker"""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": VERSION,
            "service": "legally_ai_backend"
        },
        status_code=200
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Legally AI API",
        "version": VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Example endpoint with Pydantic model (fixed warning)
from pydantic import BaseModel, ConfigDict


class AnalysisResponse(BaseModel):
    """
    Analysis response model

    Fix for Pydantic warning: Field "model_used" conflicts with protected namespace "model_"
    Solution: Set protected_namespaces to empty tuple
    """
    model_config = ConfigDict(protected_namespaces=())

    id: str
    contract_id: str
    status: str
    model_used: str  # This field caused the warning
    confidence_score: float | None = None
    result: dict | None = None


@app.get("/api/v1/analyses/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(analysis_id: str):
    """Get analysis by ID (example endpoint)"""
    # Placeholder - will be implemented with database
    return AnalysisResponse(
        id=analysis_id,
        contract_id="contract-123",
        status="completed",
        model_used="llama-3.3-70b-versatile",
        confidence_score=0.85,
        result={
            "screening_result": "no_major_issues",
            "summary": "Contract analysis complete"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
