"""
Contract Analysis Task
Async Celery task for analyzing contracts
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import uuid

from .celery_app import celery_app
from ..db.base import SessionLocal
from ..models.contract import Contract
from ..models.analysis import Analysis
from ..services.parsers import extract_text
from ..services.language import detect_language
from ..services.quality import (
    compute_quality_score,
    compute_confidence_level,
    check_hard_gates
)
from ..services.llm_router import LLMRouter
from ..services.step1_preparation import run_step1_preparation
from ..services.step2_analysis import run_step2_analysis
from ..services.formatter import format_analysis_output
from ..config import settings


def create_event(db, analysis_id: uuid.UUID, kind: str, payload: Dict = None):
    """
    Create an event for SSE progress tracking
    """
    from ..models.analysis import Base
    from sqlalchemy import Table, Column, BigInteger, Text, TIMESTAMP
    from sqlalchemy.dialects.postgresql import UUID, JSONB
    from sqlalchemy.sql import func

    # Direct SQL insert for event
    event_table = Table(
        'events',
        Base.metadata,
        Column('id', BigInteger, primary_key=True, autoincrement=True),
        Column('analysis_id', UUID(as_uuid=True), nullable=False),
        Column('kind', Text, nullable=False),
        Column('payload', JSONB, nullable=True),
        Column('created_at', TIMESTAMP(timezone=True), server_default=func.now()),
    )

    db.execute(
        event_table.insert().values(
            analysis_id=analysis_id,
            kind=kind,
            payload=payload or {}
        )
    )
    db.commit()


@celery_app.task(bind=True, name="analyze_contract")
def analyze_contract_task(
    self,
    contract_id: str,
    output_language: str = "english"
) -> Dict[str, Any]:
    """
    Analyze a contract asynchronously

    Args:
        self: Celery task instance (for state updates)
        contract_id: Contract UUID
        output_language: Language for output

    Returns:
        Analysis results
    """
    db = SessionLocal()

    try:
        contract_uuid = uuid.UUID(contract_id)

        # Get contract
        contract = db.query(Contract).filter(Contract.id == contract_uuid).first()
        if not contract:
            raise ValueError(f"Contract {contract_id} not found")

        # Create analysis record
        analysis = Analysis(
            id=uuid.uuid4(),
            contract_id=contract.id,
            status="running",
            started_at=datetime.utcnow()
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        # Update contract status
        contract.status = "analyzing"
        db.commit()

        # Event: Started
        create_event(db, analysis.id, "started", {"progress": 0})

        # Stage 1: Parse document
        self.update_state(state="PARSING", meta={"progress": 10})
        create_event(db, analysis.id, "parsing", {"progress": 10})

        file_path = Path(settings.UPLOAD_DIR) / contract.file_path
        if not file_path.exists():
            raise FileNotFoundError(f"Contract file not found: {file_path}")

        extraction = extract_text(str(file_path))
        text = extraction['text']
        quality_score_raw = extraction['quality_score']
        is_scanned = extraction['is_scanned']

        if not text or len(text) < 100:
            raise ValueError("Document appears to be empty or too short")

        # Update contract metadata
        contract.pages = extraction.get('pages')
        db.commit()

        # Stage 2: Detect language
        self.update_state(state="DETECTING_LANGUAGE", meta={"progress": 20})
        create_event(db, analysis.id, "language_detection", {"progress": 20})

        detected_lang, lang_confidence = detect_language(text)
        contract.detected_language = detected_lang
        db.commit()

        # Stage 3: Initialize LLM router
        llm_router = LLMRouter(provider=settings.LLM_PROVIDER)

        # Stage 4: Run Step 1 (Preparation)
        self.update_state(state="PREPARATION", meta={"progress": 40})
        create_event(db, analysis.id, "preparation", {"progress": 40})

        preparation_data = run_step1_preparation(
            contract_text=text,
            detected_language=detected_lang,
            quality_score=quality_score_raw,
            llm_router=llm_router
        )

        # Save step1 data
        analysis.step1_data = preparation_data
        db.commit()

        # Check hard gates
        can_proceed, gate_reason = check_hard_gates(
            quality_score_raw,
            preparation_data.get('coverage_score', 1.0)
        )

        if not can_proceed:
            analysis.status = "failed"
            analysis.error_message = f"Quality gate failed: {gate_reason}"
            analysis.completed_at = datetime.utcnow()
            contract.status = "failed"
            db.commit()

            create_event(db, analysis.id, "failed", {
                "progress": 100,
                "reason": gate_reason
            })

            return {"status": "failed", "reason": gate_reason}

        # Compute quality and confidence
        quality_score, quality_reason = compute_quality_score(
            scan_quality=quality_score_raw,
            is_scanned=is_scanned,
            is_translation=preparation_data.get('is_translation', False),
            has_original=preparation_data.get('has_original_attached', False),
            coverage=preparation_data.get('coverage_score', 1.0),
            appears_complete=preparation_data.get('appears_complete', True)
        )

        confidence_level, should_proceed = compute_confidence_level(quality_score)

        # Update contract
        contract.quality_score = quality_score
        contract.coverage_score = preparation_data.get('coverage_score', 1.0)
        contract.confidence_level = confidence_level
        contract.confidence_reason = quality_reason
        db.commit()

        if not should_proceed:
            analysis.status = "failed"
            analysis.error_message = f"Low confidence: {quality_reason}"
            analysis.confidence_score = quality_score
            analysis.completed_at = datetime.utcnow()
            contract.status = "failed"
            db.commit()

            create_event(db, analysis.id, "low_confidence", {
                "progress": 100,
                "confidence": confidence_level,
                "reason": quality_reason
            })

            return {
                "status": "failed",
                "reason": "low_confidence",
                "confidence": confidence_level
            }

        # Stage 5: Run Step 2 (Analysis)
        self.update_state(state="ANALYSIS", meta={"progress": 70})
        create_event(db, analysis.id, "analysis", {"progress": 70})

        analysis_data = run_step2_analysis(
            contract_text=text,
            preparation_data=preparation_data,
            llm_router=llm_router
        )

        # Save step2 data
        analysis.step2_data = analysis_data
        db.commit()

        # Stage 6: Format output
        self.update_state(state="FORMATTING", meta={"progress": 90})
        create_event(db, analysis.id, "formatting", {"progress": 90})

        formatted_output = format_analysis_output(
            preparation_data=preparation_data,
            analysis_data=analysis_data,
            output_language=output_language
        )

        # Save formatted output
        analysis.formatted_output = formatted_output
        analysis.confidence_score = quality_score
        analysis.model_used = f"{settings.LLM_PROVIDER}:{llm_router.model}"
        analysis.status = "succeeded"
        analysis.completed_at = datetime.utcnow()

        contract.status = "completed"

        db.commit()

        # Event: Done
        create_event(db, analysis.id, "completed", {"progress": 100})

        return {
            "status": "succeeded",
            "analysis_id": str(analysis.id),
            "confidence": confidence_level
        }

    except Exception as e:
        # Handle errors
        if 'analysis' in locals() and analysis:
            analysis.status = "failed"
            analysis.error_message = str(e)
            analysis.completed_at = datetime.utcnow()
            db.commit()

            if 'analysis' in locals():
                create_event(db, analysis.id, "error", {
                    "progress": 100,
                    "error": str(e)
                })

        if 'contract' in locals() and contract:
            contract.status = "failed"
            db.commit()

        raise

    finally:
        db.close()
