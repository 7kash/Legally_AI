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
    file_size: int
    file_path: str
    page_count: Optional[int]
    extracted_text: Optional[str]
    detected_language: Optional[str]
    jurisdiction: Optional[str]
    uploaded_at: datetime
    updated_at: datetime
    latest_analysis_id: Optional[UUID4] = None  # ID of most recent completed analysis

    model_config = {"from_attributes": True}


class ContractList(BaseModel):
    """
    List of contracts
    """
    contracts: list[ContractResponse]
    total: int
    page: int
    page_size: int
