from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional, AsyncGenerator
import uuid
from datetime import datetime
import asyncio
import json

from ..database import get_db
from ..models import Contract, Analysis, AnalysisEvent
from ..tasks.analyze_contract import analyze_contract_task

router = APIRouter()


# ===== Request/Response Models =====

class CreateAnalysisRequest(BaseModel):
    contract_id: str = Field(..., description="UUID of the contract to analyze")
    output_language: str = Field(default="english", description="Language for analysis output")

    class Config:
        json_schema_extra = {
            "example": {
                "contract_id": "123e4567-e89b-12d3-a456-426614174000",
                "output_language": "english"
            }
        }


class AnalysisResponse(BaseModel):
    id: str
    contract_id: str
    status: str
    output_language: str
    formatted_output: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ===== API Endpoints =====

@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(
    data: CreateAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new analysis for a contract and dispatch Celery task.

    This endpoint creates an Analysis record and dispatches a background task.
    The SSE endpoint can be used to stream real-time progress updates.
    """
    # Validate contract exists
    try:
        contract_uuid = uuid.UUID(data.contract_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid contract_id format"
        )

    contract = db.query(Contract).filter(Contract.id == contract_uuid).first()
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract {data.contract_id} not found"
        )

    # Create analysis record
    analysis = Analysis(
        id=uuid.uuid4(),
        contract_id=contract.id,
        status="queued",
        output_language=data.output_language,
        created_at=datetime.utcnow()
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # ✅ BUG FIX: Dispatch Celery task with analysis_id to avoid duplicate creation
    # Before: analyze_contract_task.delay(contract_id=str(contract.id), ...)
    # After: analyze_contract_task.delay(analysis_id=str(analysis.id), ...)
    analyze_contract_task.delay(
        analysis_id=str(analysis.id),  # ✅ Pass analysis_id instead of contract_id
        output_language=data.output_language
    )

    return AnalysisResponse(
        id=str(analysis.id),
        contract_id=str(analysis.contract_id),
        status=analysis.status,
        output_language=analysis.output_language,
        formatted_output=analysis.formatted_output,
        created_at=analysis.created_at,
        started_at=analysis.started_at,
        completed_at=analysis.completed_at
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Get analysis by ID"""
    try:
        analysis_uuid = uuid.UUID(analysis_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid analysis_id format"
        )

    analysis = db.query(Analysis).filter(Analysis.id == analysis_uuid).first()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )

    return AnalysisResponse(
        id=str(analysis.id),
        contract_id=str(analysis.contract_id),
        status=analysis.status,
        output_language=analysis.output_language,
        formatted_output=analysis.formatted_output,
        created_at=analysis.created_at,
        started_at=analysis.started_at,
        completed_at=analysis.completed_at
    )


@router.get("/{analysis_id}/stream")
async def stream_analysis_events(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """
    Server-Sent Events (SSE) endpoint for real-time analysis progress.

    The frontend polls this endpoint to receive status updates, progress messages,
    and results as the Celery worker processes the contract analysis.
    """
    # Validate analysis exists
    try:
        analysis_uuid = uuid.UUID(analysis_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid analysis_id format"
        )

    analysis = db.query(Analysis).filter(Analysis.id == analysis_uuid).first()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )

    async def event_generator() -> AsyncGenerator[str, None]:
        """
        Generate SSE events by polling the database for new AnalysisEvent records.

        This polls for events created by the Celery worker and streams them to the client.
        The bug fix ensures we're polling for events with the SAME analysis_id that
        the Celery worker is using to create events.
        """
        last_event_time = datetime.utcnow()
        max_iterations = 600  # 10 minutes max (600 * 1 second)
        iteration = 0

        while iteration < max_iterations:
            # Get new events since last check
            events = db.query(AnalysisEvent).filter(
                AnalysisEvent.analysis_id == analysis_uuid,
                AnalysisEvent.created_at > last_event_time
            ).order_by(AnalysisEvent.created_at).all()

            # Send events to client
            for event in events:
                event_data = {
                    "type": event.event_type,
                    "message": event.message,
                    "data": event.data,
                    "timestamp": event.created_at.isoformat()
                }
                yield f"data: {json.dumps(event_data)}\n\n"
                last_event_time = event.created_at

            # Check if analysis is complete
            db.refresh(analysis)
            if analysis.status in ["succeeded", "failed"]:
                # Send final status event
                final_event = {
                    "type": "status_change",
                    "message": f"Analysis {analysis.status}",
                    "data": {"status": analysis.status},
                    "timestamp": datetime.utcnow().isoformat()
                }
                yield f"data: {json.dumps(final_event)}\n\n"
                break

            # Wait before next poll
            await asyncio.sleep(1)
            iteration += 1

        # Timeout reached
        if iteration >= max_iterations:
            timeout_event = {
                "type": "error",
                "message": "Stream timeout reached",
                "data": {"status": "timeout"},
                "timestamp": datetime.utcnow().isoformat()
            }
            yield f"data: {json.dumps(timeout_event)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Delete analysis by ID"""
    try:
        analysis_uuid = uuid.UUID(analysis_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid analysis_id format"
        )

    analysis = db.query(Analysis).filter(Analysis.id == analysis_uuid).first()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis {analysis_id} not found"
        )

    db.delete(analysis)
    db.commit()

    return None
