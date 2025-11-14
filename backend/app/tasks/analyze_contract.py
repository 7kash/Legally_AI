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

from ..celery_app import celery_app
from ..database import SessionLocal
from ..models import Contract, Analysis, AnalysisEvent


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

        # Placeholder for now
        preparation_result = {
            "agreement_type": "Unknown",
            "parties": [],
            "jurisdiction": contract.jurisdiction or "Unknown",
            "negotiability": "medium"
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

        # Placeholder for now
        analysis_result = {
            "obligations": [],
            "rights": [],
            "risks": [],
            "payment_terms": {},
            "key_dates": []
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

        # Placeholder for now
        formatted_output = f"""
# Contract Analysis Results

## Agreement Type
{preparation_result['agreement_type']}

## Parties
- {', '.join(preparation_result['parties']) if preparation_result['parties'] else 'Not specified'}

## Jurisdiction
{preparation_result['jurisdiction']}

## Analysis
- Obligations: {len(analysis_result['obligations'])}
- Rights: {len(analysis_result['rights'])}
- Risks: {len(analysis_result['risks'])}
"""

        analysis.formatted_output = formatted_output
        analysis.status = "completed"
        analysis.completed_at = datetime.utcnow()
        db.commit()

        # Create final event
        create_event(
            db,
            analysis.id,
            event_type="status_change",
            message="Analysis completed successfully",
            data={
                "status": "completed",
                "progress": 100,
                "formatted_output": formatted_output
            }
        )

        return {
            "analysis_id": str(analysis.id),
            "status": "completed",
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
            Analysis.status.in_(["completed", "failed"])
        ).delete()

        db.commit()

        return {
            "deleted_count": deleted_count,
            "cutoff_date": cutoff_date.isoformat()
        }
    finally:
        db.close()
