"""
Contract Schemas
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional


class ContractBase(BaseModel):
    """
    Base contract schema
    """
    filename: str


class ContractUpload(BaseModel):
    """
    Contract upload response
    """
    contract_id: UUID4
    filename: str
    status: str


class ContractResponse(ContractBase):
    """
    Contract response schema
    """
    id: UUID4
    user_id: UUID4
    filename: str
    mime_type: str
    file_size_bytes: Optional[int]
    pages: Optional[int]
    detected_language: Optional[str]
    quality_score: Optional[float]
    coverage_score: Optional[float]
    confidence_level: Optional[str]
    confidence_reason: Optional[str]
    status: str
    created_at: datetime
    latest_analysis_id: Optional[UUID4] = None

    model_config = {"from_attributes": True}


class ContractList(BaseModel):
    """
    List of contracts
    """
    contracts: list[ContractResponse]
    total: int
    page: int
    page_size: int
