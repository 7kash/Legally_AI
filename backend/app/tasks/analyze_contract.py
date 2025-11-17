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
from ..config import settings
from pathlib import Path

# Import LLM analysis modules from prototype
from ..services.llm_analysis.llm_router import LLMRouter
from ..services.llm_analysis.step1_preparation import run_step1_preparation
from ..services.llm_analysis.step2_analysis import run_step2_analysis, determine_final_screening_result
from ..services.llm_analysis.language import detect_language
from ..services.llm_analysis.parsers import extract_text, detect_structure
from ..services.llm_analysis.quality import compute_quality_score, compute_confidence_level, compute_coverage_score

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
        extraction_metadata = {}

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

                # Extract text using quality-aware parser
                extraction_result = extract_text(str(file_path))

                # Store extraction metadata for quality calculation
                extraction_metadata = {
                    'quality_score': extraction_result.get('quality_score', 1.0),
                    'is_scanned': extraction_result.get('is_scanned', False),
                    'format': extraction_result.get('format', 'unknown')
                }

                # Update contract with extracted text
                contract.extracted_text = extraction_result['text']
                if 'pages' in extraction_result:
                    contract.page_count = extraction_result['pages']
                elif 'page_count' in extraction_result:
                    contract.page_count = extraction_result['page_count']
                elif 'paragraph_count' in extraction_result:
                    contract.page_count = extraction_result['paragraph_count'] // 20  # Rough estimate

                db.commit()

                quality_msg = f"quality: {extraction_metadata['quality_score']:.0%}"
                if extraction_metadata['is_scanned']:
                    quality_msg += " (scanned document)"

                create_event(
                    db,
                    analysis.id,
                    event_type="progress",
                    message=f"Extracted {len(extraction_result['text'])} characters ({quality_msg})",
                    data={"step": "extraction", "progress": 20, **extraction_metadata}
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
                extraction_metadata = {'quality_score': 0.5, 'is_scanned': False, 'format': 'unknown'}
                db.commit()
        else:
            # Text already extracted, assume good quality for existing extractions
            extraction_metadata = {'quality_score': 1.0, 'is_scanned': False, 'format': 'unknown'}

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

            # ===== Compute Document Quality Score =====
            create_event(
                db,
                analysis.id,
                event_type="progress",
                message="Assessing document quality",
                data={"step": "preparation", "progress": 32}
            )

            # Detect document structure
            structure = detect_structure(contract_text_for_llm)
            appears_complete = structure.get('appears_complete', True)

            # For now, assume no translation and all referenced documents present
            # In future, can enhance to detect translations and missing annexes
            is_translation = False
            has_original = True
            coverage = 1.0  # Assume 100% coverage for now

            # Compute quality score based on extraction quality and document completeness
            scan_quality = extraction_metadata.get('quality_score', 1.0)
            is_scanned = extraction_metadata.get('is_scanned', False)

            quality_score, quality_reason = compute_quality_score(
                scan_quality=scan_quality,
                is_scanned=is_scanned,
                is_translation=is_translation,
                has_original=has_original,
                coverage=coverage,
                appears_complete=appears_complete
            )

            logger.info(f"Quality score: {quality_score:.2f} - {quality_reason}")

            create_event(
                db,
                analysis.id,
                event_type="progress",
                message=f"Document quality: {quality_score:.0%} ({quality_reason})",
                data={"step": "preparation", "progress": 35, "quality_score": quality_score, "quality_reason": quality_reason}
            )

            # Run Step 1 preparation analysis with LLM (using redacted text)
            # Use ThreadPoolExecutor to enforce hard timeout on LLM call
            from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    run_step1_preparation,
                    contract_text=contract_text_for_llm,  # ⚠️ IMPORTANT: Use redacted text, not original
                    detected_language=detected_language,
                    quality_score=quality_score,
                    llm_router=llm_router
                )

                try:
                    # Wait max 180 seconds (3 minutes) for LLM preparation
                    preparation_result = future.result(timeout=180)
                except FuturesTimeoutError:
                    logger.error("Step 1 preparation timed out after 180 seconds")
                    raise RuntimeError("Preparation timed out - LLM service may be slow or unavailable. Please try again.")

            logger.info(f"Step 1 completed: {preparation_result.get('agreement_type', 'Unknown')}")

        except Exception as e:
            logger.error(f"Step 1 preparation failed: {e}", exc_info=True)

            # Send error event to SSE
            create_event(
                db,
                analysis.id,
                event_type="error",
                message=f"Preparation failed: {str(e)}",
                data={"step": "preparation", "error": str(e)}
            )

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

            # Use ThreadPoolExecutor to enforce hard timeout on LLM call
            from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    run_step2_analysis,
                    contract_text=contract_text_for_llm,  # ⚠️ IMPORTANT: Use redacted text, not original
                    preparation_data=preparation_result,
                    llm_router=llm_router,
                    output_language=output_language  # Pass output language for bilingual quotes
                )

                try:
                    # Wait max 180 seconds (3 minutes) for LLM analysis
                    analysis_result = future.result(timeout=180)
                except FuturesTimeoutError:
                    logger.error("Step 2 analysis timed out after 180 seconds")
                    raise RuntimeError("Analysis timed out - LLM service may be slow or unavailable. Please try again.")

            logger.info(f"Step 2 completed: Found {len(analysis_result.get('obligations', []))} obligations, {len(analysis_result.get('risks', []))} risks")

        except Exception as e:
            logger.error(f"Step 2 analysis failed: {e}", exc_info=True)

            # Send error event to SSE
            create_event(
                db,
                analysis.id,
                event_type="error",
                message=f"Analysis failed: {str(e)}",
                data={"step": "analysis", "error": str(e)}
            )

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
                "title": "Your Obligations",
                "content": analysis_result['obligations'] if analysis_result['obligations'] else ["No obligations identified"]
            },
            "rights": {
                "title": "Your Rights",
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
            "suggestions": {
                "title": "Suggested Changes",
                "content": analysis_result.get('suggestions', [])
            },
            "mitigations": {
                "title": "Risk Mitigations",
                "content": analysis_result.get('mitigations', [])
            },
            "calendar": {
                "title": "Key Dates & Deadlines",
                "content": analysis_result.get('calendar', [])
            }
        }

        # Calculate and store screening result
        llm_screening = analysis_result.get('screening_result', 'recommended_to_address')
        quality_score_value = preparation_result.get('quality_score', quality_score)  # Use calculated quality_score
        coverage_score_value = preparation_result.get('coverage_score', coverage)  # Use calculated coverage

        final_screening = determine_final_screening_result(
            llm_screening,
            quality_score_value,
            coverage_score_value
        )

        # Calculate confidence level using quality module
        confidence, should_proceed = compute_confidence_level(quality_score_value)

        logger.info(f"Confidence level: {confidence} (quality: {quality_score_value:.2f}, screening: {final_screening})")

        # Store quality metrics to database
        analysis.screening_result = final_screening
        analysis.quality_score = int(quality_score_value * 100)  # Convert 0.9 -> 90
        analysis.confidence_level = confidence

        # Store directly as dict (JSON column)
        analysis.formatted_output = formatted_output

        # ===== ELI5: Generate Simplified Version =====
        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Generating simplified version (ELI5)",
            data={"step": "eli5", "progress": 90}
        )

        try:
            from ..services.llm_analysis.eli5_service import simplify_full_analysis

            # Generate ELI5 simplified version
            simplified_output = simplify_full_analysis(
                analysis_result=formatted_output,
                sections_to_simplify=['obligations', 'rights', 'risks', 'mitigations']
            )

            # Store ELI5 version
            analysis.formatted_output_eli5 = simplified_output
            logger.info("ELI5 simplified version generated successfully")

            create_event(
                db,
                analysis.id,
                event_type="progress",
                message="Simplified version ready",
                data={"step": "eli5", "progress": 95}
            )
        except Exception as e:
            logger.error(f"ELI5 generation failed: {e}", exc_info=True)
            # Don't fail the whole analysis if ELI5 fails
            create_event(
                db,
                analysis.id,
                event_type="progress",
                message=f"Note: Simplified version not available",
                data={"step": "eli5", "progress": 95, "error": str(e)}
            )

        analysis.status = "succeeded"
        analysis.completed_at = datetime.utcnow()
        db.commit()

        # Extract and store deadlines
        try:
            from ..services.deadline_service import extract_deadlines_from_analysis
            deadlines = extract_deadlines_from_analysis(
                analysis_id=analysis.id,
                contract_id=analysis.contract_id,
                user_id=contract.user_id,
                analysis_result=analysis_result,
                db=db
            )
            logger.info(f"Extracted {len(deadlines)} deadlines from analysis")
        except Exception as e:
            logger.error(f"Failed to extract deadlines: {e}", exc_info=True)
            # Don't fail the whole analysis if deadline extraction fails

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
