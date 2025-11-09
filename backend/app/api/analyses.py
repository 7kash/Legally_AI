"""
Analyses API
Endpoints for contract analysis and results
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import uuid
import asyncio
import json
from typing import AsyncGenerator
from datetime import datetime

from ..db.base import get_db
from ..models.user import User
from ..models.contract import Contract
from ..models.analysis import Analysis
from ..schemas.analysis import AnalysisCreate, AnalysisResponse, AnalysisFeedback
from ..core.deps import get_current_user, check_analysis_limit
from ..tasks.analyze_contract import analyze_contract_task

router = APIRouter()


@router.post("", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
    data: AnalysisCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Start contract analysis

    Args:
        data: Analysis creation data (contract_id, output_language)
        current_user: Current authenticated user
        db: Database session

    Returns:
        Analysis object with queued status

    Raises:
        HTTPException: If contract not found or analysis limit reached
    """
    # Check analysis limit for free tier
    check_analysis_limit(current_user)

    # Verify contract exists and belongs to user
    contract = db.query(Contract).filter(
        Contract.id == data.contract_id,
        Contract.user_id == current_user.id
    ).first()

    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contract not found"
        )

    # Check if analysis already exists for this contract
    existing_analysis = db.query(Analysis).filter(
        Analysis.contract_id == contract.id,
        Analysis.status.in_(["queued", "running", "succeeded"])
    ).first()

    if existing_analysis:
        # Return existing analysis
        return AnalysisResponse.model_validate(existing_analysis)

    # Create analysis record
    analysis = Analysis(
        id=uuid.uuid4(),
        contract_id=contract.id,
        status="queued"
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # Dispatch Celery task
    analyze_contract_task.delay(
        contract_id=str(contract.id),
        output_language=data.output_language
    )

    # Increment user's contract count (for free tier limit)
    if current_user.tier == "free":
        current_user.contracts_analyzed += 1
        db.commit()

    return AnalysisResponse.model_validate(analysis)


@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get analysis results

    Args:
        analysis_id: Analysis ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Analysis with results

    Raises:
        HTTPException: If analysis not found or access denied
    """
    # Get analysis with contract (for user verification)
    analysis = db.query(Analysis).join(Contract).filter(
        Analysis.id == analysis_id,
        Contract.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )

    return AnalysisResponse.model_validate(analysis)


async def event_generator(
    analysis_id: uuid.UUID,
    db: Session
) -> AsyncGenerator[str, None]:
    """
    Generate SSE events for analysis progress

    Args:
        analysis_id: Analysis ID
        db: Database session

    Yields:
        SSE formatted events
    """
    last_event_id = 0

    while True:
        # Get new events since last check
        from sqlalchemy import text

        result = db.execute(
            text("""
                SELECT id, kind, payload, created_at
                FROM events
                WHERE analysis_id = :analysis_id
                  AND id > :last_id
                ORDER BY id ASC
            """),
            {"analysis_id": str(analysis_id), "last_id": last_event_id}
        )

        events = result.fetchall()

        for event in events:
            event_id, kind, payload, created_at = event
            last_event_id = event_id

            # Format SSE message
            data = {
                "kind": kind,
                "payload": payload or {},
                "timestamp": created_at.isoformat()
            }

            yield f"data: {json.dumps(data)}\n\n"

            # Check if analysis is done
            if kind in ["completed", "failed", "error", "low_confidence"]:
                yield "event: close\ndata: {}\n\n"
                return

        # Check analysis status
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if analysis and analysis.status in ["succeeded", "failed"]:
            # Send final event if not already sent
            if not events or events[-1][1] not in ["completed", "failed", "error"]:
                data = {
                    "kind": analysis.status,
                    "payload": {"status": analysis.status},
                    "timestamp": datetime.utcnow().isoformat()
                }
                yield f"data: {json.dumps(data)}\n\n"
                yield "event: close\ndata: {}\n\n"
            return

        # Wait before next check
        await asyncio.sleep(1)


@router.get("/{analysis_id}/stream")
async def stream_analysis_progress(
    analysis_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Stream analysis progress via Server-Sent Events (SSE)

    Args:
        analysis_id: Analysis ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        SSE stream of progress events

    Raises:
        HTTPException: If analysis not found or access denied
    """
    # Verify access
    analysis = db.query(Analysis).join(Contract).filter(
        Analysis.id == analysis_id,
        Contract.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )

    return StreamingResponse(
        event_generator(analysis_id, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/{analysis_id}/feedback", status_code=status.HTTP_204_NO_CONTENT)
async def submit_feedback(
    analysis_id: uuid.UUID,
    feedback: AnalysisFeedback,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit feedback on analysis quality

    Args:
        analysis_id: Analysis ID
        feedback: Feedback data
        current_user: Current authenticated user
        db: Database session

    Raises:
        HTTPException: If analysis not found or access denied
    """
    # Verify access
    analysis = db.query(Analysis).join(Contract).filter(
        Analysis.id == analysis_id,
        Contract.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )

    # Create feedback record
    from sqlalchemy import Table, Column, Text, Boolean, TIMESTAMP
    from sqlalchemy.dialects.postgresql import UUID as PGUUID
    from sqlalchemy.sql import func

    # Direct SQL insert for feedback
    from ..models.analysis import Base

    feedback_table = Table(
        'feedback',
        Base.metadata,
        Column('id', PGUUID(as_uuid=True)),
        Column('analysis_id', PGUUID(as_uuid=True)),
        Column('user_id', PGUUID(as_uuid=True)),
        Column('section', Text),
        Column('is_correct', Boolean),
        Column('comment', Text),
        Column('created_at', TIMESTAMP(timezone=True)),
    )

    db.execute(
        feedback_table.insert().values(
            id=uuid.uuid4(),
            analysis_id=analysis_id,
            user_id=current_user.id,
            section=feedback.section,
            is_correct=feedback.is_correct,
            comment=feedback.comment,
            created_at=func.now()
        )
    )
    db.commit()

    return None


@router.get("/{analysis_id}/export/pdf")
async def export_analysis_pdf(
    analysis_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export analysis as PDF

    Args:
        analysis_id: Analysis ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        PDF file download

    Raises:
        HTTPException: If analysis not found or access denied
    """
    from fastapi.responses import Response
    from ..utils.export import generate_pdf

    # Verify access
    analysis = db.query(Analysis).join(Contract).filter(
        Analysis.id == analysis_id,
        Contract.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )

    # Check if analysis is complete
    if analysis.status != "succeeded":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Analysis is not complete (status: {analysis.status})"
        )

    # Get contract for filename
    contract = db.query(Contract).filter(Contract.id == analysis.contract_id).first()

    # Prepare analysis data
    analysis_data = {
        'contract_filename': contract.filename if contract else 'Unknown',
        'status': analysis.status,
        'results': analysis.results or {},
        'analysis_id': str(analysis.id),
        'created_at': analysis.created_at.isoformat() if analysis.created_at else None,
    }

    # Generate PDF
    pdf_bytes = generate_pdf(analysis_data)

    # Return PDF file
    filename = f"contract_analysis_{analysis_id}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": "application/pdf"
        }
    )


@router.get("/{analysis_id}/export/docx")
async def export_analysis_docx(
    analysis_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export analysis as DOCX

    Args:
        analysis_id: Analysis ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        DOCX file download

    Raises:
        HTTPException: If analysis not found or access denied
    """
    from fastapi.responses import Response
    from ..utils.export import generate_docx

    # Verify access
    analysis = db.query(Analysis).join(Contract).filter(
        Analysis.id == analysis_id,
        Contract.user_id == current_user.id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )

    # Check if analysis is complete
    if analysis.status != "succeeded":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Analysis is not complete (status: {analysis.status})"
        )

    # Get contract for filename
    contract = db.query(Contract).filter(Contract.id == analysis.contract_id).first()

    # Prepare analysis data
    analysis_data = {
        'contract_filename': contract.filename if contract else 'Unknown',
        'status': analysis.status,
        'results': analysis.results or {},
        'analysis_id': str(analysis.id),
        'created_at': analysis.created_at.isoformat() if analysis.created_at else None,
    }

    # Generate DOCX
    docx_bytes = generate_docx(analysis_data)

    # Return DOCX file
    filename = f"contract_analysis_{analysis_id}.docx"

    return Response(
        content=docx_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        }
    )
