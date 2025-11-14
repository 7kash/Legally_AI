"""
Security Utilities
Password hashing and JWT token generation
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Args:
        data: Data to encode in the token
        expires_delta: Token expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token

    Args:
        token: JWT token to decode

    Returns:
        Decoded token data or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def create_verification_token(email: str, expires_hours: int = 24) -> str:
    """
    Create a token for email verification

    Args:
        email: User's email address
        expires_hours: Token expiration time in hours

    Returns:
        Encoded JWT token
    """
    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    to_encode = {
        "sub": email,
        "type": "email_verification",
        "exp": expire,
        "iat": datetime.utcnow()
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_password_reset_token(email: str, expires_hours: int = 1) -> str:
    """
    Create a token for password reset

    Args:
        email: User's email address
        expires_hours: Token expiration time in hours (default 1 hour for security)

    Returns:
        Encoded JWT token
    """
    expire = datetime.utcnow() + timedelta(hours=expires_hours)
    to_encode = {
        "sub": email,
        "type": "password_reset",
        "exp": expire,
        "iat": datetime.utcnow()
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_token(token: str, token_type: str) -> Optional[str]:
    """
    Verify and decode a token (email verification or password reset)

    Args:
        token: JWT token to verify
        token_type: Expected token type ("email_verification" or "password_reset")

    Returns:
        Email from token if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Verify token type
        if payload.get("type") != token_type:
            return None

        # Return the email (stored in "sub")
        return payload.get("sub")
    except JWTError:
        return None
