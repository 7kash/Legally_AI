"""
Analysis Schemas
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, Any


class AnalysisCreate(BaseModel):
    """
    Analysis creation schema
    """
    contract_id: UUID4
    output_language: str = "english"


class AnalysisProgress(BaseModel):
    """
    Analysis progress event (SSE)
    """
    status: str  # 'queued' | 'parsing' | 'preparation' | 'analysis' | 'formatting' | 'done' | 'failed'
    progress: int  # 0-100
    message: str


class AnalysisResponse(BaseModel):
    """
    Analysis response schema
    """
    id: UUID4
    contract_id: UUID4
    status: str
    confidence_score: Optional[float]
    model_used: Optional[str]
    tokens_used: Optional[int]
    cost_cents: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration_seconds: Optional[float]

    # Analysis data (only when completed)
    step1_data: Optional[dict[str, Any]] = None
    step2_data: Optional[dict[str, Any]] = None
    formatted_output: Optional[dict[str, Any]] = None

    model_config = {"from_attributes": True}


class AnalysisFeedback(BaseModel):
    """
    User feedback on analysis quality
    """
    section: str  # Which section the feedback is about
    is_correct: bool
    comment: Optional[str] = None
