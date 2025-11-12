"""
Analysis Model
Database model for contract analyses
"""

from sqlalchemy import Column, String, Integer, Float, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from typing import Optional
import uuid

from ..db.base import Base


class Analysis(Base):
    """
    Contract analysis model
    """

    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False)

    # Analysis data (JSON)
    step1_data = Column(JSONB, nullable=True)  # Preparation data
    step2_data = Column(JSONB, nullable=True)  # Analysis data
    formatted_output = Column(JSONB, nullable=True)  # Final formatted output

    # LLM metadata
    model_used = Column(Text, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    cost_cents = Column(Integer, nullable=True)

    # Quality
    confidence_score = Column(Float, nullable=True)

    # Status
    status = Column(String(20), default="queued", nullable=False)  # 'queued' | 'running' | 'succeeded' | 'failed'
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    started_at = Column(TIMESTAMP(timezone=True), nullable=True)
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    # contract = relationship("Contract", back_populates="analyses")
    # events = relationship("Event", back_populates="analysis", cascade="all, delete-orphan")
    # feedback = relationship("Feedback", back_populates="analysis", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Analysis(id={self.id}, status={self.status})>"

    @property
    def duration_seconds(self) -> Optional[float]:
        """
        Calculate analysis duration in seconds
        """
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
