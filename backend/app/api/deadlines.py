"""
Deadlines API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import uuid

from ..database import get_db
from ..models import Deadline, DeadlineType
from ..api.auth import get_current_user, User

router = APIRouter(prefix="/deadlines", tags=["deadlines"])


# Pydantic schemas
class DeadlineResponse(BaseModel):
    id: uuid.UUID
    contract_id: uuid.UUID
    analysis_id: Optional[uuid.UUID]
    deadline_type: str
    title: str
    description: Optional[str]
    date: Optional[datetime]
    date_formula: Optional[str]
    is_recurring: bool
    is_completed: bool
    completed_at: Optional[datetime]
    source_section: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class DeadlineUpdate(BaseModel):
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


@router.get("", response_model=List[DeadlineResponse])
async def get_deadlines(
    upcoming_only: bool = Query(False, description="Only return upcoming deadlines"),
    days_ahead: int = Query(30, description="Days ahead to look for upcoming deadlines"),
    contract_id: Optional[uuid.UUID] = Query(None, description="Filter by contract ID"),
    is_completed: Optional[bool] = Query(None, description="Filter by completion status"),
    deadline_type: Optional[str] = Query(None, description="Filter by deadline type"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all deadlines for the current user

    Query Parameters:
    - upcoming_only: Only show deadlines within next N days
    - days_ahead: Number of days to look ahead (default 30)
    - contract_id: Filter by specific contract
    - is_completed: Filter by completion status
    - deadline_type: Filter by deadline type (payment, renewal, etc.)
    """
    query = db.query(Deadline).filter(Deadline.user_id == current_user.id)

    # Apply filters
    if contract_id:
        query = query.filter(Deadline.contract_id == contract_id)

    if is_completed is not None:
        query = query.filter(Deadline.is_completed == is_completed)

    if deadline_type:
        try:
            dt = DeadlineType(deadline_type)
            query = query.filter(Deadline.deadline_type == dt)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid deadline_type: {deadline_type}")

    if upcoming_only:
        cutoff_date = datetime.utcnow() + timedelta(days=days_ahead)
        query = query.filter(
            Deadline.date != None,
            Deadline.date <= cutoff_date,
            Deadline.is_completed == False
        )

    # Order by date (nulls last)
    deadlines = query.order_by(Deadline.date.asc().nullslast(), Deadline.created_at.desc()).all()

    return deadlines


@router.get("/upcoming", response_model=List[DeadlineResponse])
async def get_upcoming_deadlines(
    days: int = Query(30, description="Number of days ahead to check"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get upcoming deadlines within the next N days
    """
    cutoff_date = datetime.utcnow() + timedelta(days=days)

    deadlines = db.query(Deadline).filter(
        Deadline.user_id == current_user.id,
        Deadline.is_completed == False,
        Deadline.date != None,
        Deadline.date <= cutoff_date
    ).order_by(Deadline.date.asc()).all()

    return deadlines


@router.get("/{deadline_id}", response_model=DeadlineResponse)
async def get_deadline(
    deadline_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific deadline by ID
    """
    deadline = db.query(Deadline).filter(
        Deadline.id == deadline_id,
        Deadline.user_id == current_user.id
    ).first()

    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")

    return deadline


@router.patch("/{deadline_id}", response_model=DeadlineResponse)
async def update_deadline(
    deadline_id: uuid.UUID,
    update: DeadlineUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a deadline (mark as completed, etc.)
    """
    deadline = db.query(Deadline).filter(
        Deadline.id == deadline_id,
        Deadline.user_id == current_user.id
    ).first()

    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")

    # Update fields
    if update.is_completed is not None:
        deadline.is_completed = update.is_completed
        if update.is_completed and not deadline.completed_at:
            deadline.completed_at = datetime.utcnow()
        elif not update.is_completed:
            deadline.completed_at = None

    if update.completed_at is not None:
        deadline.completed_at = update.completed_at

    deadline.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(deadline)

    return deadline


@router.delete("/{deadline_id}")
async def delete_deadline(
    deadline_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a deadline
    """
    deadline = db.query(Deadline).filter(
        Deadline.id == deadline_id,
        Deadline.user_id == current_user.id
    ).first()

    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")

    db.delete(deadline)
    db.commit()

    return {"message": "Deadline deleted successfully"}


@router.get("/{deadline_id}/ics")
async def export_deadline_ics(
    deadline_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export deadline as .ics calendar file
    """
    from fastapi.responses import Response
    from ..utils.calendar_export import create_ics_from_deadline

    deadline = db.query(Deadline).filter(
        Deadline.id == deadline_id,
        Deadline.user_id == current_user.id
    ).first()

    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")

    if not deadline.date:
        raise HTTPException(status_code=400, detail="Deadline has no specific date")

    ics_content = create_ics_from_deadline(deadline)

    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={
            "Content-Disposition": f"attachment; filename=deadline_{deadline.id}.ics"
        }
    )


@router.get("/export/all-ics")
async def export_all_deadlines_ics(
    upcoming_only: bool = Query(True),
    days_ahead: int = Query(90),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export all deadlines as single .ics calendar file
    """
    from fastapi.responses import Response
    from ..utils.calendar_export import create_ics_from_deadlines

    query = db.query(Deadline).filter(
        Deadline.user_id == current_user.id,
        Deadline.date != None
    )

    if upcoming_only:
        cutoff_date = datetime.utcnow() + timedelta(days=days_ahead)
        query = query.filter(
            Deadline.is_completed == False,
            Deadline.date <= cutoff_date
        )

    deadlines = query.order_by(Deadline.date.asc()).all()

    if not deadlines:
        raise HTTPException(status_code=404, detail="No deadlines to export")

    ics_content = create_ics_from_deadlines(deadlines)

    return Response(
        content=ics_content,
        media_type="text/calendar",
        headers={
            "Content-Disposition": "attachment; filename=contract_deadlines.ics"
        }
    )
