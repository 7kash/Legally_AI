"""
Feedback API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import uuid

from ..database import get_db
from ..models import Feedback, FeedbackType, FeedbackSection
from ..api.auth import get_current_user, User

router = APIRouter(prefix="/feedback", tags=["feedback"])


# Pydantic schemas
class FeedbackCreate(BaseModel):
    analysis_id: uuid.UUID
    contract_id: uuid.UUID
    feedback_type: str = Field(default="accuracy", description="Type of feedback")
    section: str = Field(..., description="Section of the analysis")
    item_index: Optional[int] = Field(None, description="Index of item within section")
    is_accurate: Optional[bool] = Field(None, description="Was this accurate?")
    quality_rating: Optional[int] = Field(None, ge=1, le=5, description="Quality rating (1-5)")
    comment: Optional[str] = Field(None, max_length=2000, description="Free-text comment")

    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "123e4567-e89b-12d3-a456-426614174000",
                "contract_id": "123e4567-e89b-12d3-a456-426614174001",
                "feedback_type": "accuracy",
                "section": "obligations",
                "item_index": 0,
                "is_accurate": True,
                "comment": "This was very helpful!"
            }
        }


class FeedbackResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    analysis_id: uuid.UUID
    contract_id: uuid.UUID
    feedback_type: str
    section: str
    item_index: Optional[int]
    is_accurate: Optional[bool]
    quality_rating: Optional[int]
    comment: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FeedbackStats(BaseModel):
    """Statistics for feedback on an analysis"""
    total_feedback_count: int
    accuracy_positive: int
    accuracy_negative: int
    average_quality_rating: Optional[float]
    section_stats: dict


@router.post("", response_model=FeedbackResponse, status_code=201)
async def create_feedback(
    data: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit feedback on an analysis section or item

    Allows users to provide feedback on analysis results to improve accuracy
    and calibrate confidence scores over time.
    """
    # Validate feedback_type
    try:
        feedback_type = FeedbackType(data.feedback_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid feedback_type. Must be one of: {[t.value for t in FeedbackType]}"
        )

    # Validate section
    try:
        section = FeedbackSection(data.section)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid section. Must be one of: {[s.value for s in FeedbackSection]}"
        )

    # Create feedback
    feedback = Feedback(
        id=uuid.uuid4(),
        user_id=current_user.id,
        analysis_id=data.analysis_id,
        contract_id=data.contract_id,
        feedback_type=feedback_type,
        section=section,
        item_index=data.item_index,
        is_accurate=data.is_accurate,
        quality_rating=data.quality_rating,
        comment=data.comment,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    return feedback


@router.get("", response_model=List[FeedbackResponse])
async def get_feedback(
    analysis_id: Optional[uuid.UUID] = Query(None, description="Filter by analysis ID"),
    contract_id: Optional[uuid.UUID] = Query(None, description="Filter by contract ID"),
    section: Optional[str] = Query(None, description="Filter by section"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get feedback submissions

    Retrieve feedback submissions filtered by various criteria.
    Regular users can only see their own feedback.
    """
    query = db.query(Feedback).filter(Feedback.user_id == current_user.id)

    # Apply filters
    if analysis_id:
        query = query.filter(Feedback.analysis_id == analysis_id)

    if contract_id:
        query = query.filter(Feedback.contract_id == contract_id)

    if section:
        try:
            section_enum = FeedbackSection(section)
            query = query.filter(Feedback.section == section_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid section: {section}")

    feedback_list = query.order_by(Feedback.created_at.desc()).all()
    return feedback_list


@router.get("/stats/{analysis_id}", response_model=FeedbackStats)
async def get_feedback_stats(
    analysis_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get aggregated feedback statistics for an analysis

    Provides summary statistics about feedback received for a specific analysis.
    """
    feedback_list = db.query(Feedback).filter(
        Feedback.analysis_id == analysis_id,
        Feedback.user_id == current_user.id
    ).all()

    if not feedback_list:
        return FeedbackStats(
            total_feedback_count=0,
            accuracy_positive=0,
            accuracy_negative=0,
            average_quality_rating=None,
            section_stats={}
        )

    # Calculate statistics
    accuracy_positive = sum(1 for f in feedback_list if f.is_accurate is True)
    accuracy_negative = sum(1 for f in feedback_list if f.is_accurate is False)

    quality_ratings = [f.quality_rating for f in feedback_list if f.quality_rating is not None]
    average_quality = sum(quality_ratings) / len(quality_ratings) if quality_ratings else None

    # Section stats
    section_stats = {}
    for section in FeedbackSection:
        section_feedback = [f for f in feedback_list if f.section == section]
        if section_feedback:
            section_stats[section.value] = {
                "count": len(section_feedback),
                "accuracy_positive": sum(1 for f in section_feedback if f.is_accurate is True),
                "accuracy_negative": sum(1 for f in section_feedback if f.is_accurate is False),
            }

    return FeedbackStats(
        total_feedback_count=len(feedback_list),
        accuracy_positive=accuracy_positive,
        accuracy_negative=accuracy_negative,
        average_quality_rating=average_quality,
        section_stats=section_stats
    )


@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a feedback submission

    Users can delete their own feedback.
    """
    feedback = db.query(Feedback).filter(
        Feedback.id == feedback_id,
        Feedback.user_id == current_user.id
    ).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    db.delete(feedback)
    db.commit()

    return {"message": "Feedback deleted successfully"}
