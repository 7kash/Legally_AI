"""
Authentication API
Endpoints for user registration, login, and profile management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid

from ..db.base import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from ..core.security import verify_password, get_password_hash, create_access_token
from ..core.deps import get_current_user

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        JWT token and user data

    Raises:
        HTTPException: If email already exists
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    new_user = User(
        id=uuid.uuid4(),
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        is_active=True,
        is_verified=False,
        is_superuser=False,
        tier="free",
        contracts_analyzed=0
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    access_token = create_access_token(data={"sub": str(new_user.id)})

    # Prepare response
    user_response = UserResponse(
        id=new_user.id,
        email=new_user.email,
        tier=new_user.tier,
        contracts_analyzed=new_user.contracts_analyzed,
        analyses_remaining=new_user.analyses_remaining,
        is_active=new_user.is_active,
        is_verified=new_user.is_verified,
        created_at=new_user.created_at
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password

    Args:
        credentials: Login credentials
        db: Database session

    Returns:
        JWT token and user data

    Raises:
        HTTPException: If credentials are invalid
    """
    # Get user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    # Prepare response
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        tier=user.tier,
        contracts_analyzed=user.contracts_analyzed,
        analyses_remaining=user.analyses_remaining,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user profile

    Args:
        current_user: Current authenticated user

    Returns:
        User profile data
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        tier=current_user.tier,
        contracts_analyzed=current_user.contracts_analyzed,
        analyses_remaining=current_user.analyses_remaining,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at
    )


@router.post("/logout")
async def logout():
    """
    Logout (client-side token deletion)

    Returns:
        Success message
    """
    # JWT tokens are stateless, so logout is handled client-side
    # Client should delete the token from storage
    return {"message": "Successfully logged out"}
