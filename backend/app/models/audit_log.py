"""
Audit Log Model

Tracks all data access and operations for compliance (GDPR Article 30 - Records of Processing Activities)
"""

from sqlalchemy import Column, String, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from ..database import Base


class AuditLog(Base):
    """
    Audit log entry for tracking data access and operations.

    GDPR Compliance:
    - Article 30: Records of processing activities
    - Article 32: Security of processing
    - Article 5(2): Accountability principle
    """
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Who performed the action
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)  # Nullable for system actions
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(500), nullable=True)

    # What action was performed
    action = Column(String(100), nullable=False, index=True)  # e.g., "contract_upload", "contract_view", "contract_delete"
    resource_type = Column(String(50), nullable=False)  # e.g., "contract", "analysis", "user"
    resource_id = Column(UUID(as_uuid=True), nullable=True, index=True)  # ID of the affected resource

    # Action details
    status = Column(String(20), nullable=False)  # "success", "failure", "unauthorized"
    details = Column(JSON, nullable=True)  # Additional context (e.g., error message, changed fields)

    # When it happened
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Performance tracking
    duration_ms = Column(Integer, nullable=True)  # How long the operation took

    def __repr__(self):
        return f"<AuditLog {self.action} on {self.resource_type} by user {self.user_id} at {self.created_at}>"
