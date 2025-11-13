"""
Contract Model
Database model for uploaded contracts
"""

from sqlalchemy import Column, String, Integer, Float, Text, TIMESTAMP, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from ..db.base import Base


class Contract(Base):
    """
    Uploaded contract model
    """

    __tablename__ = "contracts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # File info
    filename = Column(Text, nullable=False)
    mime_type = Column(Text, nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    file_path = Column(Text, nullable=False)
    pages = Column(Integer, nullable=True)

    # Analysis metadata
    detected_language = Column(String(20), nullable=True)  # 'russian' | 'serbian' | 'french' | 'english'
    quality_score = Column(Float, nullable=True)
    coverage_score = Column(Float, nullable=True)
    confidence_level = Column(String(20), nullable=True)  # 'High' | 'Medium' | 'Low'
    confidence_reason = Column(Text, nullable=True)

    # Status
    status = Column(String(20), default="uploaded", nullable=False)  # 'uploaded' | 'analyzing' | 'completed' | 'failed'

    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    analyses = relationship("Analysis", back_populates="contract", cascade="all, delete-orphan")
    # deadlines = relationship("Deadline", back_populates="contract", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index("idx_user_created", "user_id", "created_at"),
    )

    def __repr__(self):
        return f"<Contract(id={self.id}, filename={self.filename}, status={self.status})>"
