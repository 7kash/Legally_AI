"""
Account Management API
Endpoints for account details, profile updates, GDPR compliance
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional

from ..db.base import get_db
from ..models.user import User
from ..models.contract import Contract
from ..models.analysis import Analysis
from ..schemas.user import AccountDetails, AccountUpdate, AccountExportData, UserResponse
from ..core.deps import get_current_user
from ..core.security import verify_password, get_password_hash

router = APIRouter()


@router.get("", response_model=AccountDetails)
async def get_account_details(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get account details with usage statistics

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        Account details with contract and analysis counts
    """
    # Count total contracts uploaded by user
    total_contracts = db.query(func.count(Contract.id)).filter(
        Contract.user_id == current_user.id
    ).scalar() or 0

    # Count total analyses performed
    total_analyses = db.query(func.count(Analysis.id)).join(Contract).filter(
        Contract.user_id == current_user.id
    ).scalar() or 0

    # Determine tier limit
    tier_limit = -1 if current_user.tier == "premium" else 3

    # Build response
    account_data = {
        "id": current_user.id,
        "email": current_user.email,
        "tier": current_user.tier,
        "contracts_analyzed": current_user.contracts_analyzed,
        "analyses_remaining": current_user.analyses_remaining,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
        "total_contracts": total_contracts,
        "total_analyses": total_analyses,
        "tier_limit": tier_limit,
    }

    return AccountDetails(**account_data)


@router.patch("", response_model=UserResponse)
async def update_account(
    update_data: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update account profile

    Args:
        update_data: Profile update data (email, password)
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user object

    Raises:
        HTTPException: If validation fails or email already exists
    """
    # Update email if provided
    if update_data.email is not None and update_data.email != current_user.email:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == update_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        current_user.email = update_data.email
        # Mark as unverified if email changed
        current_user.is_verified = False

    # Update password if provided
    if update_data.new_password is not None:
        # Require current password for security
        if not update_data.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password required to set new password"
            )

        # Verify current password
        if not verify_password(update_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )

        # Update password
        current_user.hashed_password = get_password_hash(update_data.new_password)

    # Commit changes
    db.commit()
    db.refresh(current_user)

    return UserResponse.model_validate(current_user)


@router.get("/export", response_model=AccountExportData)
async def export_account_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export all account data (GDPR compliance)

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        Complete account data export in JSON format
    """
    # Get user data
    user_data = {
        "id": str(current_user.id),
        "email": current_user.email,
        "tier": current_user.tier,
        "contracts_analyzed": current_user.contracts_analyzed,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "updated_at": current_user.updated_at.isoformat() if current_user.updated_at else None,
    }

    # Get all contracts
    contracts = db.query(Contract).filter(Contract.user_id == current_user.id).all()
    contracts_data = [
        {
            "id": str(contract.id),
            "filename": contract.filename,
            "file_type": contract.file_type,
            "file_size": contract.file_size,
            "uploaded_at": contract.uploaded_at.isoformat() if contract.uploaded_at else None,
        }
        for contract in contracts
    ]

    # Get all analyses
    analyses = db.query(Analysis).join(Contract).filter(
        Contract.user_id == current_user.id
    ).all()
    analyses_data = [
        {
            "id": str(analysis.id),
            "contract_id": str(analysis.contract_id),
            "status": analysis.status,
            "results": analysis.results,
            "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
            "completed_at": analysis.completed_at.isoformat() if analysis.completed_at else None,
        }
        for analysis in analyses
    ]

    # Get all feedback
    from sqlalchemy import text
    feedback_result = db.execute(
        text("""
            SELECT f.id, f.analysis_id, f.section, f.is_correct, f.comment, f.created_at
            FROM feedback f
            JOIN analyses a ON f.analysis_id = a.id
            JOIN contracts c ON a.contract_id = c.id
            WHERE c.user_id = :user_id
            ORDER BY f.created_at DESC
        """),
        {"user_id": str(current_user.id)}
    )

    feedback_data = [
        {
            "id": str(row[0]),
            "analysis_id": str(row[1]),
            "section": row[2],
            "is_correct": row[3],
            "comment": row[4],
            "created_at": row[5].isoformat() if row[5] else None,
        }
        for row in feedback_result.fetchall()
    ]

    # Build export data
    export_data = AccountExportData(
        user=user_data,
        contracts=contracts_data,
        analyses=analyses_data,
        feedback=feedback_data,
        exported_at=datetime.utcnow()
    )

    return export_data


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete account and all associated data (GDPR compliance)

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        None (204 No Content)

    Notes:
        - Deletes user account
        - Cascades to delete contracts, analyses, events, feedback
        - Permanent deletion (cannot be undone)
    """
    # Delete user (cascade will handle related data)
    # Order: feedback -> events -> analyses -> contracts -> user

    # The database schema should have cascade deletes configured,
    # but we'll be explicit for GDPR compliance documentation

    from sqlalchemy import text

    # Get all contract IDs for this user
    contracts = db.query(Contract).filter(Contract.user_id == current_user.id).all()
    contract_ids = [str(c.id) for c in contracts]

    if contract_ids:
        # Get all analysis IDs
        analyses = db.query(Analysis).filter(
            Analysis.contract_id.in_([c.id for c in contracts])
        ).all()
        analysis_ids = [str(a.id) for a in analyses]

        if analysis_ids:
            # Delete feedback
            db.execute(
                text("DELETE FROM feedback WHERE analysis_id = ANY(:analysis_ids)"),
                {"analysis_ids": analysis_ids}
            )

            # Delete events
            db.execute(
                text("DELETE FROM events WHERE analysis_id = ANY(:analysis_ids)"),
                {"analysis_ids": analysis_ids}
            )

            # Delete analyses
            db.query(Analysis).filter(Analysis.id.in_([a.id for a in analyses])).delete(
                synchronize_session=False
            )

        # Delete contracts
        db.query(Contract).filter(Contract.id.in_([c.id for c in contracts])).delete(
            synchronize_session=False
        )

    # Delete user
    db.delete(current_user)
    db.commit()

    return None
