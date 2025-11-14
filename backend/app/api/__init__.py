from fastapi import APIRouter

from . import analyses, auth, account, contracts

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(account.router, prefix="/account", tags=["account"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(analyses.router, prefix="/analyses", tags=["analyses"])

__all__ = ["api_router"]
