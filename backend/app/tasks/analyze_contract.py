"""
Celery task for contract analysis.

BUG FIX: This task now receives analysis_id instead of contract_id to avoid
creating duplicate Analysis records. The API endpoint creates the Analysis record
and passes its ID to this task.
"""

from celery import Task
from sqlalchemy.orm import Session
from typing import Dict, Any
import uuid
from datetime import datetime
import traceback
import logging

logger = logging.getLogger(__name__)

from ..celery_app import celery_app
from ..database import SessionLocal
from ..models import Contract, Analysis, AnalysisEvent
from ..services.document_parser import extract_text
from ..config import settings
from pathlib import Path

# Import LLM analysis modules from prototype
from ..services.llm_analysis.llm_router import LLMRouter
from ..services.llm_analysis.step1_preparation import run_step1_preparation
from ..services.llm_analysis.step2_analysis import run_step2_analysis
from ..services.llm_analysis.language import detect_language
from ..services.llm_analysis.parsers import extract_text as extract_text_with_quality
from ..services.llm_analysis.quality import compute_quality_score, compute_confidence_level

# Import PII redaction for GDPR compliance
from ..utils.pii_redactor import redact_pii


class DatabaseTask(Task):
    """Base task class that handles database sessions"""
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            self._session.close()

    @property
    def session(self) -> Session:
        if self._session is None:
            self._session = SessionLocal()
        return self._session


def create_event(db: Session, analysis_id: uuid.UUID, event_type: str, message: str, data: Dict = None):
    """Helper function to create SSE events"""
    event = AnalysisEvent(
        analysis_id=analysis_id,
        event_type=event_type,
        message=message,
        data=data,
        created_at=datetime.utcnow()
    )
    db.add(event)
    db.commit()


@celery_app.task(bind=True, base=DatabaseTask, name="analyze_contract")
def analyze_contract_task(
    self,
    analysis_id: str,  # ✅ BUG FIX: Receive analysis_id instead of contract_id
    output_language: str = "english"
) -> Dict[str, Any]:
    """
    Analyze a contract asynchronously.

    ✅ BUG FIX APPLIED:
    - This task now receives analysis_id (not contract_id)
    - It fetches the existing Analysis record (doesn't create a new one)
    - This ensures the SSE stream polls for events with the correct analysis_id

    Args:
        analysis_id: UUID of the Analysis record (created by API endpoint)
        output_language: Language for output (default: "english")

    Returns:
        Dict with analysis results
    """
    db = self.session

    try:
        # ✅ BUG FIX: Parse analysis_id instead of contract_id
        try:
            analysis_uuid = uuid.UUID(analysis_id)
        except ValueError:
            raise ValueError(f"Invalid analysis_id format: {analysis_id}")

        # ✅ BUG FIX: Get existing analysis record (created by API endpoint)
        # Before: Created NEW Analysis with uuid.uuid4()
        # After: Fetch existing Analysis by ID
        analysis = db.query(Analysis).filter(Analysis.id == analysis_uuid).first()
        if not analysis:
            raise ValueError(f"Analysis {analysis_id} not found")

        # Get contract through the analysis relationship
        contract = db.query(Contract).filter(Contract.id == analysis.contract_id).first()
        if not contract:
            raise ValueError(f"Contract {analysis.contract_id} not found")

        # ✅ BUG FIX: Update analysis status to running (don't create new record)
        # Before: analysis = Analysis(id=uuid.uuid4(), contract_id=..., status="running")
        # After: analysis.status = "running"
        analysis.status = "running"
        analysis.started_at = datetime.utcnow()
        db.commit()

        # Create event: Analysis started
        create_event(
            db,
            analysis.id,
            event_type="status_change",
            message="Analysis started",
            data={"status": "running"}
        )

        # ===== STEP 0: Text Extraction (if needed) =====
        if not contract.extracted_text:
            create_event(
                db,
                analysis.id,
                event_type="progress",
                message="Extracting text from document",
                data={"step": "extraction", "progress": 10}
            )

            try:
                # Build full file path
                file_path = Path(settings.UPLOAD_DIR) / contract.file_path

                # Extract text using document parser
                extraction_result = extract_text(str(file_path))

                # Update contract with extracted text
                contract.extracted_text = extraction_result['text']
                if 'page_count' in extraction_result:
                    contract.page_count = extraction_result['page_count']
                elif 'paragraph_count' in extraction_result:
                    contract.page_count = extraction_result['paragraph_count'] // 20  # Rough estimate

                db.commit()

                create_event(
                    db,
                    analysis.id,
                    event_type="progress",
                    message=f"Extracted {len(extraction_result['text'])} characters from document",
                    data={"step": "extraction", "progress": 20}
                )
            except Exception as e:
                logger.error(f"Text extraction failed: {e}")
                # Log error but continue with empty text
                create_event(
                    db,
                    analysis.id,
                    event_type="progress",
                    message=f"Warning: Text extraction failed: {str(e)}",
                    data={"step": "extraction", "progress": 20, "error": str(e)}
                )
                contract.extracted_text = ""
                db.commit()

        # ===== GDPR COMPLIANCE: PII REDACTION =====
        # Redact personally identifiable information before sending to LLM
        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Protecting personal data (GDPR compliance)",
            data={"step": "pii_redaction", "progress": 22}
        )

        original_text = contract.extracted_text or ""
        redacted_text, pii_summary = redact_pii(original_text)

        # Log PII redaction summary
        if pii_summary:
            logger.info(f"PII redaction summary: {pii_summary}")
            create_event(
                db,
                analysis.id,
                event_type="progress",
                message=f"Protected {sum(pii_summary.values())} personal data items",
                data={"step": "pii_redaction", "progress": 24, "pii_summary": pii_summary}
            )
        else:
            logger.info("No PII detected in contract text")

        # Use redacted text for LLM analysis (NEVER send original text with PII)
        contract_text_for_llm = redacted_text

        # ===== STEP 1: Document Preparation =====
        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Starting document preparation with LLM",
            data={"step": "preparation", "progress": 25}
        )

        try:
            # Initialize LLM router
            llm_router = LLMRouter()

            # Detect language of contract text (use redacted text)
            detected_language, lang_confidence = detect_language(contract_text_for_llm)
            logger.info(f"Detected language: {detected_language} (confidence: {lang_confidence})")

            create_event(
                db,
                analysis.id,
                event_type="progress",
                message=f"Detected language: {detected_language}",
                data={"step": "preparation", "progress": 30}
            )

            # Compute quality score
            # For simplicity, assume high quality for now (can enhance later)
            quality_score = 0.9

            # Run Step 1 preparation analysis with LLM (using redacted text)
            preparation_result = run_step1_preparation(
                contract_text=contract_text_for_llm,  # ⚠️ IMPORTANT: Use redacted text, not original
                detected_language=detected_language,
                quality_score=quality_score,
                llm_router=llm_router
            )

            logger.info(f"Step 1 completed: {preparation_result.get('agreement_type', 'Unknown')}")

        except Exception as e:
            logger.error(f"Step 1 preparation failed: {e}", exc_info=True)
            # Fall back to placeholder if LLM fails
            preparation_result = {
                "agreement_type": "Error: Could not analyze",
                "parties": [],
                "jurisdiction": contract.jurisdiction or "Unknown",
                "negotiability": "medium",
                "error": str(e)
            }
            create_event(
                db,
                analysis.id,
                event_type="progress",
                message=f"Warning: LLM preparation failed, using fallback: {str(e)}",
                data={"step": "preparation", "progress": 35, "error": str(e)}
            )

        # Store directly as dict (JSON column)
        analysis.preparation_result = preparation_result
        db.commit()

        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Document preparation completed",
            data={"step": "preparation", "progress": 40, "result": preparation_result}
        )

        # ===== STEP 2: Contract Analysis =====
        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Starting detailed contract analysis with LLM",
            data={"step": "analysis", "progress": 45}
        )

        try:
            # Run Step 2 analysis with LLM (reuse llm_router from Step 1)
            if 'llm_router' not in locals():
                llm_router = LLMRouter()

            analysis_result = run_step2_analysis(
                contract_text=contract_text_for_llm,  # ⚠️ IMPORTANT: Use redacted text, not original
                preparation_data=preparation_result,
                llm_router=llm_router
            )

            logger.info(f"Step 2 completed: Found {len(analysis_result.get('obligations', []))} obligations, {len(analysis_result.get('risks', []))} risks")

        except Exception as e:
            logger.error(f"Step 2 analysis failed: {e}", exc_info=True)
            # Fall back to placeholder if LLM fails
            analysis_result = {
                "obligations": [],
                "rights": [],
                "risks": [{"description": f"Error during analysis: {str(e)}", "recommendation": "Please try again"}],
                "payment_terms": {},
                "key_dates": []
            }
            create_event(
                db,
                analysis.id,
                event_type="progress",
                message=f"Warning: LLM analysis failed, using fallback: {str(e)}",
                data={"step": "analysis", "progress": 60, "error": str(e)}
            )

        # Store directly as dict (JSON column)
        analysis.analysis_result = analysis_result
        db.commit()

        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Contract analysis completed",
            data={"step": "analysis", "progress": 65, "result": analysis_result}
        )

        # ===== STEP 3: Format Output =====
        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Formatting results",
            data={"step": "formatting", "progress": 85}
        )

        # TODO: Import and use formatter from prototype
        # from prototype.src.formatter import format_analysis
        # formatted_output = format_analysis(preparation_result, analysis_result, output_language)

        # Create structured JSON output
        formatted_output = {
            "agreement_type": {
                "title": "Agreement Type",
                "content": preparation_result['agreement_type']
            },
            "parties": {
                "title": "Parties",
                "content": preparation_result['parties'] if preparation_result['parties'] else ["Not specified"]
            },
            "jurisdiction": {
                "title": "Jurisdiction",
                "content": preparation_result['jurisdiction']
            },
            "obligations": {
                "title": "Obligations",
                "content": analysis_result['obligations'] if analysis_result['obligations'] else ["No obligations identified"]
            },
            "rights": {
                "title": "Rights",
                "content": analysis_result['rights'] if analysis_result['rights'] else ["No rights identified"]
            },
            "risks": {
                "title": "Risks & Concerns",
                "content": analysis_result['risks'] if analysis_result['risks'] else ["No risks identified"]
            },
            "payment_terms": {
                "title": "Payment Terms",
                "content": analysis_result.get('payment_terms', {})
            },
            "key_dates": {
                "title": "Key Dates",
                "content": analysis_result.get('key_dates', [])
            }
        }

        # Store directly as dict (JSON column)
        analysis.formatted_output = formatted_output
        analysis.status = "succeeded"
        analysis.completed_at = datetime.utcnow()
        db.commit()

        # Create final event
        create_event(
            db,
            analysis.id,
            event_type="status_change",
            message="Analysis completed successfully",
            data={
                "status": "succeeded",
                "progress": 100,
                "formatted_output": formatted_output
            }
        )

        return {
            "analysis_id": str(analysis.id),
            "status": "succeeded",
            "preparation_result": preparation_result,
            "analysis_result": analysis_result
        }

    except Exception as e:
        # Handle errors
        error_message = str(e)
        error_traceback = traceback.format_exc()

        # Update analysis status
        if 'analysis' in locals() and analysis:
            analysis.status = "failed"
            analysis.error_message = error_message
            analysis.error_traceback = error_traceback
            analysis.completed_at = datetime.utcnow()
            db.commit()

            # Create error event
            create_event(
                db,
                analysis.id,
                event_type="error",
                message=f"Analysis failed: {error_message}",
                data={"status": "failed", "error": error_message}
            )

        # Re-raise for Celery error handling
        raise


@celery_app.task(name="cleanup_old_analyses")
def cleanup_old_analyses():
    """
    Periodic task to clean up old analysis records.

    This can be scheduled with Celery Beat to run daily.
    """
    db = SessionLocal()
    try:
        # Delete analyses older than 30 days
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=30)

        deleted_count = db.query(Analysis).filter(
            Analysis.created_at < cutoff_date,
            Analysis.status.in_(["succeeded", "failed"])
        ).delete()

        db.commit()

        return {
            "deleted_count": deleted_count,
            "cutoff_date": cutoff_date.isoformat()
        }
    finally:
        db.close()
