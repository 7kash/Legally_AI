"""
User Schemas
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """
    Base user schema
    """
    email: EmailStr


class UserCreate(UserBase):
    """
    User creation schema
    """
    password: str


class UserLogin(BaseModel):
    """
    User login schema
    """
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """
    User update schema
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """
    User response schema
    """
    id: UUID4
    tier: str
    contracts_analyzed: int
    analyses_remaining: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """
    Authentication token response
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class AccountDetails(UserResponse):
    """
    Extended account details with statistics
    """
    total_contracts: int
    total_analyses: int
    tier_limit: int  # -1 for unlimited (premium), 3 for free


class AccountUpdate(BaseModel):
    """
    Account profile update schema
    """
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None


class AccountExportData(BaseModel):
    """
    GDPR data export schema
    """
    user: dict
    contracts: list
    analyses: list
    feedback: list
    exported_at: datetime
