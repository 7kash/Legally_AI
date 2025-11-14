"""
Custom Exceptions
Application-specific exceptions
"""

from fastapi import HTTPException, status


class AnalysisLimitExceeded(HTTPException):
    """
    Raised when user exceeds free tier analysis limit
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Free tier limit reached. Upgrade to Premium for unlimited analyses."
        )


class ContractNotFound(HTTPException):
    """
    Raised when contract is not found
    """

    def __init__(self, contract_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract {contract_id} not found"
        )


class AnalysisNotFound(HTTPException):
    """
    Raised when analysis is not found
    """

    def __init__(self, analysis_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )


class InvalidCredentials(HTTPException):
    """
    Raised when authentication credentials are invalid
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )


class UserAlreadyExists(HTTPException):
    """
    Raised when attempting to register with existing email
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


class FileTypeNotAllowed(HTTPException):
    """
    Raised when uploaded file type is not allowed
    """

    def __init__(self, file_type: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_type} not allowed. Allowed types: .pdf, .docx"
        )


class FileTooLarge(HTTPException):
    """
    Raised when uploaded file exceeds size limit
    """

    def __init__(self, max_size_mb: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {max_size_mb}MB limit"
        )
