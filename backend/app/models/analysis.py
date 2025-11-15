from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True)

    # Status: queued, running, succeeded, failed
    status = Column(String(50), nullable=False, default="queued", index=True)

    # Output language
    output_language = Column(String(50), nullable=False, default="english")

    # Results - stored as JSON
    preparation_result = Column(JSON, nullable=True)  # Step 1 results
    analysis_result = Column(JSON, nullable=True)     # Step 2 results
    formatted_output = Column(JSON, nullable=True)    # Final formatted output

    # Quality metrics
    quality_score = Column(Integer, nullable=True)
    confidence_level = Column(String(50), nullable=True)
    screening_result = Column(String(50), nullable=True)

    # Error tracking
    error_message = Column(Text, nullable=True)
    error_traceback = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    contract = relationship("Contract", back_populates="analyses")
    events = relationship("AnalysisEvent", back_populates="analysis", cascade="all, delete-orphan", order_by="AnalysisEvent.created_at")
    deadlines = relationship("Deadline", back_populates="analysis", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Analysis(id={self.id}, status={self.status})>"


class AnalysisEvent(Base):
    """SSE events for real-time progress updates"""
    __tablename__ = "analysis_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False, index=True)

    # Event information
    event_type = Column(String(50), nullable=False)  # status_change, progress, error, result
    message = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationship
    analysis = relationship("Analysis", back_populates="events")

    def __repr__(self):
        return f"<AnalysisEvent(id={self.id}, type={self.event_type})>"
