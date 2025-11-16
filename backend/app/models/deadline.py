"""
Deadline model for contract deadlines tracking
"""

from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from datetime import datetime

from ..database import Base


class DeadlineType(str, enum.Enum):
    """Deadline types"""
    PAYMENT = "payment"
    RENEWAL = "renewal"
    NOTICE = "notice"
    TERMINATION = "termination"
    OPTION_EXERCISE = "option_exercise"
    OBLIGATION = "obligation"
    OTHER = "other"


class Deadline(Base):
    """
    Deadline model
    Stores important deadlines extracted from contract analyses
    """
    __tablename__ = "deadlines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id", ondelete="CASCADE"), nullable=False, index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Deadline info
    deadline_type = Column(SQLEnum(DeadlineType), nullable=False, default=DeadlineType.OTHER)
    title = Column(String(200), nullable=False)  # e.g., "Pay monthly rent"
    description = Column(Text, nullable=True)  # Additional details

    # Date/formula
    date = Column(DateTime, nullable=True)  # Specific date if known
    date_formula = Column(String(200), nullable=True)  # e.g., "Monthly on 20th", "30 days before lease end"

    # Status
    is_recurring = Column(Boolean, default=False)  # Monthly, yearly, etc.
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    # Metadata
    source_section = Column(String(100), nullable=True)  # Which analysis section this came from
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    contract = relationship("Contract", back_populates="deadlines")
    analysis = relationship("Analysis", back_populates="deadlines")
    user = relationship("User", back_populates="deadlines")

    def __repr__(self):
        return f"<Deadline {self.title} - {self.date or self.date_formula}>"
