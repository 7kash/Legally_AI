"""
Feedback Model
Stores user feedback on analysis results for confidence calibration
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from ..database import Base


class FeedbackType(str, enum.Enum):
    """Types of feedback that can be submitted"""
    ACCURACY = "accuracy"  # Was this accurate?
    QUALITY = "quality"    # Overall quality rating
    MISSING = "missing"    # Something is missing
    INCORRECT = "incorrect"  # Something is wrong
    OTHER = "other"        # Other feedback


class FeedbackSection(str, enum.Enum):
    """Sections that can receive feedback"""
    OBLIGATIONS = "obligations"
    RIGHTS = "rights"
    RISKS = "risks"
    PAYMENT_TERMS = "payment_terms"
    CALENDAR = "calendar"
    MITIGATIONS = "mitigations"
    SUGGESTIONS = "suggestions"
    SCREENING = "screening"
    OVERALL = "overall"


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id", ondelete="CASCADE"), nullable=False, index=True)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True)

    # Feedback details
    feedback_type = Column(SQLEnum(FeedbackType), nullable=False, default=FeedbackType.ACCURACY)
    section = Column(SQLEnum(FeedbackSection), nullable=False, default=FeedbackSection.OVERALL)
    item_index = Column(Integer, nullable=True)  # Which item in the section (0-indexed)

    # Ratings and content
    is_accurate = Column(Boolean, nullable=True)  # True = accurate, False = not accurate, None = not rated
    quality_rating = Column(Integer, nullable=True)  # 1-5 stars
    comment = Column(Text, nullable=True)  # Free-text feedback

    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="feedback")
    analysis = relationship("Analysis", back_populates="feedback")
    contract = relationship("Contract", back_populates="feedback")

    def __repr__(self):
        return f"<Feedback {self.id} - {self.section} - {self.feedback_type}>"
