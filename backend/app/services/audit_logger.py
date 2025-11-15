"""
Audit Logger Service

Provides easy-to-use functions for logging audit events throughout the application.
"""

from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from ..models.audit_log import AuditLog


class AuditLogger:
    """
    Service for creating audit log entries.

    Usage:
        audit = AuditLogger(db, user_id="...", ip_address="...", user_agent="...")
        audit.log_contract_upload(contract_id, status="success")
        audit.log_contract_view(contract_id)
        audit.log_contract_delete(contract_id)
    """

    def __init__(
        self,
        db: Session,
        user_id: Optional[uuid.UUID] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        self.db = db
        self.user_id = user_id
        self.ip_address = ip_address
        self.user_agent = user_agent

    def _log(
        self,
        action: str,
        resource_type: str,
        resource_id: Optional[uuid.UUID] = None,
        status: str = "success",
        details: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[int] = None
    ) -> AuditLog:
        """
        Create an audit log entry.

        Args:
            action: The action performed (e.g., "contract_upload", "analysis_view")
            resource_type: Type of resource (e.g., "contract", "analysis", "user")
            resource_id: ID of the affected resource
            status: "success", "failure", or "unauthorized"
            details: Additional context as a dictionary
            duration_ms: How long the operation took in milliseconds

        Returns:
            The created AuditLog entry
        """
        log_entry = AuditLog(
            user_id=self.user_id,
            ip_address=self.ip_address,
            user_agent=self.user_agent,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            status=status,
            details=details,
            duration_ms=duration_ms,
            created_at=datetime.utcnow()
        )

        self.db.add(log_entry)
        self.db.commit()
        self.db.refresh(log_entry)

        return log_entry

    # ===== Contract Operations =====

    def log_contract_upload(
        self,
        contract_id: uuid.UUID,
        filename: str,
        file_size: int,
        status: str = "success",
        error: Optional[str] = None
    ) -> AuditLog:
        """Log contract file upload"""
        details = {
            "filename": filename,
            "file_size": file_size
        }
        if error:
            details["error"] = error

        return self._log(
            action="contract_upload",
            resource_type="contract",
            resource_id=contract_id,
            status=status,
            details=details
        )

    def log_contract_view(
        self,
        contract_id: uuid.UUID,
        status: str = "success"
    ) -> AuditLog:
        """Log viewing a contract"""
        return self._log(
            action="contract_view",
            resource_type="contract",
            resource_id=contract_id,
            status=status
        )

    def log_contract_download(
        self,
        contract_id: uuid.UUID,
        status: str = "success"
    ) -> AuditLog:
        """Log downloading a contract file"""
        return self._log(
            action="contract_download",
            resource_type="contract",
            resource_id=contract_id,
            status=status
        )

    def log_contract_delete(
        self,
        contract_id: uuid.UUID,
        filename: str,
        status: str = "success"
    ) -> AuditLog:
        """Log contract deletion (GDPR Right to Erasure)"""
        return self._log(
            action="contract_delete",
            resource_type="contract",
            resource_id=contract_id,
            status=status,
            details={"filename": filename}
        )

    # ===== Analysis Operations =====

    def log_analysis_create(
        self,
        analysis_id: uuid.UUID,
        contract_id: uuid.UUID,
        status: str = "success"
    ) -> AuditLog:
        """Log creation of new analysis"""
        return self._log(
            action="analysis_create",
            resource_type="analysis",
            resource_id=analysis_id,
            status=status,
            details={"contract_id": str(contract_id)}
        )

    def log_analysis_view(
        self,
        analysis_id: uuid.UUID,
        status: str = "success"
    ) -> AuditLog:
        """Log viewing analysis results"""
        return self._log(
            action="analysis_view",
            resource_type="analysis",
            resource_id=analysis_id,
            status=status
        )

    def log_analysis_export(
        self,
        analysis_id: uuid.UUID,
        export_format: str,  # "pdf", "docx", "json"
        status: str = "success"
    ) -> AuditLog:
        """Log exporting analysis results"""
        return self._log(
            action="analysis_export",
            resource_type="analysis",
            resource_id=analysis_id,
            status=status,
            details={"format": export_format}
        )

    def log_analysis_delete(
        self,
        analysis_id: uuid.UUID,
        status: str = "success"
    ) -> AuditLog:
        """Log analysis deletion"""
        return self._log(
            action="analysis_delete",
            resource_type="analysis",
            resource_id=analysis_id,
            status=status
        )

    # ===== User Operations =====

    def log_user_login(
        self,
        user_id: uuid.UUID,
        status: str = "success",
        error: Optional[str] = None
    ) -> AuditLog:
        """Log user login attempt"""
        details = {}
        if error:
            details["error"] = error

        return self._log(
            action="user_login",
            resource_type="user",
            resource_id=user_id,
            status=status,
            details=details if details else None
        )

    def log_user_logout(
        self,
        user_id: uuid.UUID
    ) -> AuditLog:
        """Log user logout"""
        return self._log(
            action="user_logout",
            resource_type="user",
            resource_id=user_id,
            status="success"
        )

    def log_user_register(
        self,
        user_id: uuid.UUID,
        email: str,
        status: str = "success"
    ) -> AuditLog:
        """Log user registration"""
        return self._log(
            action="user_register",
            resource_type="user",
            resource_id=user_id,
            status=status,
            details={"email": email}
        )

    def log_user_delete(
        self,
        user_id: uuid.UUID,
        email: str,
        status: str = "success"
    ) -> AuditLog:
        """Log user account deletion (GDPR Right to Erasure)"""
        return self._log(
            action="user_delete",
            resource_type="user",
            resource_id=user_id,
            status=status,
            details={"email": email}
        )

    def log_user_data_access(
        self,
        user_id: uuid.UUID,
        data_type: str,  # What data was accessed
        status: str = "success"
    ) -> AuditLog:
        """Log data access request (GDPR Right to Access)"""
        return self._log(
            action="user_data_access",
            resource_type="user",
            resource_id=user_id,
            status=status,
            details={"data_type": data_type}
        )

    # ===== PII Protection =====

    def log_pii_redaction(
        self,
        contract_id: uuid.UUID,
        pii_summary: Dict[str, int],  # {"email": 2, "phone": 1, ...}
        total_redacted: int
    ) -> AuditLog:
        """Log PII redaction (GDPR compliance)"""
        return self._log(
            action="pii_redaction",
            resource_type="contract",
            resource_id=contract_id,
            status="success",
            details={
                "pii_summary": pii_summary,
                "total_items_redacted": total_redacted
            }
        )

    # ===== Security Events =====

    def log_unauthorized_access(
        self,
        resource_type: str,
        resource_id: Optional[uuid.UUID],
        attempted_action: str,
        reason: str
    ) -> AuditLog:
        """Log unauthorized access attempt (security monitoring)"""
        return self._log(
            action=f"{attempted_action}_unauthorized",
            resource_type=resource_type,
            resource_id=resource_id,
            status="unauthorized",
            details={"reason": reason}
        )

    def log_rate_limit_exceeded(
        self,
        endpoint: str
    ) -> AuditLog:
        """Log rate limit exceeded (abuse prevention)"""
        return self._log(
            action="rate_limit_exceeded",
            resource_type="system",
            status="failure",
            details={"endpoint": endpoint}
        )


# Helper function to create an audit logger
def get_audit_logger(
    db: Session,
    user_id: Optional[uuid.UUID] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> AuditLogger:
    """
    Create an audit logger instance.

    Usage in FastAPI endpoint:
        from fastapi import Request
        audit = get_audit_logger(
            db,
            user_id=current_user.id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
        audit.log_contract_view(contract_id)
    """
    return AuditLogger(db, user_id, ip_address, user_agent)
