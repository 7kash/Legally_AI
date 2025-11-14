from fastapi import APIRouter

from . import analyses

api_router = APIRouter()

api_router.include_router(analyses.router, prefix="/analyses", tags=["analyses"])

__all__ = ["api_router"]
