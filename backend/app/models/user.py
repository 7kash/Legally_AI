"""
User Model
Database model for user accounts
"""

from sqlalchemy import Column, String, Boolean, Integer, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from ..database import Base


class User(Base):
    """
    User account model
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(Text, unique=True, nullable=False, index=True)
    hashed_password = Column(Text, nullable=False)

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # Subscription
    tier = Column(String(20), default="free", nullable=False)  # 'free' | 'premium'
    contracts_analyzed = Column(Integer, default=0, nullable=False)

    # Stripe
    stripe_customer_id = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, tier={self.tier})>"

    @property
    def has_free_analyses_remaining(self) -> bool:
        """
        Check if user has free analyses remaining
        """
        if self.tier == "premium":
            return True
        return self.contracts_analyzed < 3

    @property
    def analyses_remaining(self) -> int:
        """
        Number of free analyses remaining
        """
        if self.tier == "premium":
            return -1  # Unlimited
        return max(0, 3 - self.contracts_analyzed)
