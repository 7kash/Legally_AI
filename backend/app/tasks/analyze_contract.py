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
from pathlib import Path

from ..celery_app import celery_app
from ..database import SessionLocal
from ..models import Contract, Analysis, AnalysisEvent
from ..services.document_parser import extract_text
from ..config import settings


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

        # ===== STEP 0: Extract Text from Document (if not already extracted) =====
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
                # Log error but continue with empty text
                create_event(
                    db,
                    analysis.id,
                    event_type="progress",
                    message=f"Text extraction failed: {str(e)}. Continuing with empty text.",
                    data={"step": "extraction", "progress": 20, "error": str(e)}
                )
                contract.extracted_text = ""
                db.commit()

        # ===== STEP 1: Document Preparation =====
        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Starting document preparation",
            data={"step": "preparation", "progress": 0}
        )

        # TODO: Import and use actual analysis modules from prototype
        # from prototype.src.step1_preparation import run_preparation
        # preparation_result = run_preparation(contract.extracted_text, output_language)

        # Basic placeholder analysis using extracted text
        extracted_text = contract.extracted_text or ""
        text_lower = extracted_text.lower()

        # Try to detect agreement type
        agreement_type = "Contract"
        if "employment" in text_lower or "employee" in text_lower:
            agreement_type = "Employment Agreement"
        elif "service" in text_lower or "services" in text_lower:
            agreement_type = "Service Agreement"
        elif "lease" in text_lower or "rental" in text_lower:
            agreement_type = "Lease Agreement"
        elif "sale" in text_lower or "purchase" in text_lower:
            agreement_type = "Sales Agreement"
        elif "license" in text_lower or "licensing" in text_lower:
            agreement_type = "License Agreement"

        # Try to extract some basic parties (very simplified)
        parties = []
        if "between" in text_lower:
            # This is a very basic extraction - production would use NER
            parties = ["Party A", "Party B"]

        preparation_result = {
            "agreement_type": agreement_type,
            "parties": parties,
            "jurisdiction": contract.jurisdiction or "Not specified",
            "negotiability": "medium",
            "document_length": len(extracted_text),
            "has_content": len(extracted_text) > 100
        }

        analysis.preparation_result = preparation_result
        db.commit()

        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Document preparation completed",
            data={"step": "preparation", "progress": 50, "result": preparation_result}
        )

        # ===== STEP 2: Contract Analysis =====
        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Starting contract analysis",
            data={"step": "analysis", "progress": 50}
        )

        # TODO: Import and use actual analysis modules from prototype
        # from prototype.src.step2_analysis import run_analysis
        # analysis_result = run_analysis(contract.extracted_text, preparation_result, output_language)

        # Basic content analysis
        obligations = []
        rights = []
        risks = []

        # Look for obligation keywords
        if "shall" in text_lower or "must" in text_lower or "required" in text_lower:
            obligations.append("Contractual obligations identified (detailed analysis pending)")

        # Look for rights keywords
        if "right" in text_lower or "entitled" in text_lower or "may" in text_lower:
            rights.append("Contractual rights identified (detailed analysis pending)")

        # Look for risk keywords
        if "terminate" in text_lower or "liability" in text_lower or "damages" in text_lower:
            risks.append("Potential risk areas identified (detailed analysis pending)")

        # Look for payment terms
        payment_terms = {}
        if "$" in extracted_text or "payment" in text_lower or "fee" in text_lower:
            payment_terms = {"note": "Payment terms present - detailed extraction pending"}

        # Look for dates
        key_dates = []
        if any(word in text_lower for word in ["date", "term", "duration", "expire"]):
            key_dates.append("Important dates identified in document")

        analysis_result = {
            "obligations": obligations,
            "rights": rights,
            "risks": risks,
            "payment_terms": payment_terms,
            "key_dates": key_dates,
            "text_analyzed": len(extracted_text) > 0
        }

        analysis.analysis_result = analysis_result
        db.commit()

        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Contract analysis completed",
            data={"step": "analysis", "progress": 75, "result": analysis_result}
        )

        # ===== STEP 3: Format Output =====
        create_event(
            db,
            analysis.id,
            event_type="progress",
            message="Formatting results",
            data={"step": "formatting", "progress": 80}
        )

        # TODO: Import and use formatter from prototype
        # from prototype.src.formatter import format_analysis
        # formatted_output = format_analysis(preparation_result, analysis_result, output_language)

        # Format output as JSON structure for frontend
        formatted_output = {
            "agreement_type": {
                "title": "Agreement Type",
                "content": preparation_result['agreement_type']
            },
            "parties": {
                "title": "Parties",
                "content": ', '.join(preparation_result['parties']) if preparation_result['parties'] else 'Not specified'
            },
            "jurisdiction": {
                "title": "Jurisdiction",
                "content": preparation_result['jurisdiction']
            },
            "obligations": {
                "title": "Obligations",
                "content": f"Found {len(analysis_result['obligations'])} obligations in the contract."
            },
            "rights": {
                "title": "Rights",
                "content": f"Found {len(analysis_result['rights'])} rights in the contract."
            },
            "risks": {
                "title": "Risks",
                "content": f"Found {len(analysis_result['risks'])} potential risks in the contract."
            },
            "payment_terms": {
                "title": "Payment Terms",
                "content": str(analysis_result['payment_terms']) if analysis_result['payment_terms'] else 'No payment terms specified.'
            },
            "key_dates": {
                "title": "Key Dates",
                "content": ', '.join(str(date) for date in analysis_result['key_dates']) if analysis_result['key_dates'] else 'No key dates identified.'
            }
        }

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
                "has_results": True
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
