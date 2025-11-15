"""
Deadline extraction and management service
Extracts deadlines from analysis results and stores them in the database
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from dateutil import parser as date_parser
import uuid

from ..models import Deadline, DeadlineType
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


def parse_date(date_string: str) -> Optional[datetime]:
    """
    Parse date string to datetime object
    Handles various date formats
    """
    if not date_string:
        return None

    try:
        # Try to parse as ISO format first
        return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        pass

    try:
        # Try flexible date parsing
        return date_parser.parse(date_string)
    except (ValueError, TypeError):
        return None


def categorize_deadline_type(event: str, source: str = None) -> DeadlineType:
    """
    Categorize deadline based on event description and source
    """
    event_lower = event.lower() if event else ""

    if any(word in event_lower for word in ['pay', 'payment', 'rent', 'fee', 'invoice']):
        return DeadlineType.PAYMENT
    elif any(word in event_lower for word in ['renew', 'renewal', 'extend', 'extension']):
        return DeadlineType.RENEWAL
    elif any(word in event_lower for word in ['notice', 'notify', 'inform']):
        return DeadlineType.NOTICE
    elif any(word in event_lower for word in ['terminate', 'termination', 'cancel', 'end']):
        return DeadlineType.TERMINATION
    elif any(word in event_lower for word in ['option', 'choose', 'elect']):
        return DeadlineType.OPTION_EXERCISE
    elif source == 'obligations':
        return DeadlineType.OBLIGATION
    else:
        return DeadlineType.OTHER


def is_recurring(date_formula: str) -> bool:
    """
    Determine if a date formula represents a recurring deadline
    """
    if not date_formula:
        return False

    formula_lower = date_formula.lower()
    recurring_keywords = ['monthly', 'weekly', 'yearly', 'annually', 'quarterly', 'daily']

    return any(keyword in formula_lower for keyword in recurring_keywords)


def extract_deadlines_from_analysis(
    analysis_id: uuid.UUID,
    contract_id: uuid.UUID,
    user_id: uuid.UUID,
    analysis_result: Dict[str, Any],
    db: Session
) -> List[Deadline]:
    """
    Extract deadlines from analysis results and create Deadline objects

    Args:
        analysis_id: Analysis UUID
        contract_id: Contract UUID
        user_id: User UUID
        analysis_result: Complete analysis results dictionary
        db: Database session

    Returns:
        List of created Deadline objects
    """
    deadlines = []

    try:
        # Extract from calendar section
        calendar = analysis_result.get('calendar', [])
        if calendar:
            for item in calendar:
                if not isinstance(item, dict):
                    continue

                date_str = item.get('date_or_formula') or item.get('date')
                event = item.get('event') or item.get('description')

                if not date_str or not event:
                    continue

                # Parse date if it's a specific date
                parsed_date = parse_date(date_str)
                date_formula = None if parsed_date else date_str

                # Create deadline
                deadline = Deadline(
                    id=uuid.uuid4(),
                    contract_id=contract_id,
                    analysis_id=analysis_id,
                    user_id=user_id,
                    deadline_type=categorize_deadline_type(event, 'calendar'),
                    title=event[:200],  # Truncate to fit column
                    date=parsed_date,
                    date_formula=date_formula,
                    is_recurring=is_recurring(date_formula or ""),
                    is_completed=False,
                    source_section='calendar',
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )

                db.add(deadline)
                deadlines.append(deadline)

        # Extract from obligations (time-sensitive actions)
        obligations = analysis_result.get('obligations', [])
        if obligations:
            for idx, obligation in enumerate(obligations):
                if not isinstance(obligation, dict):
                    continue

                action = obligation.get('action')
                time_window = obligation.get('time_window')

                if not action:
                    continue

                # Only create deadline if there's a specific time window
                if time_window and time_window.lower() not in ['ongoing', 'not stated', 'none']:
                    parsed_date = parse_date(time_window)
                    date_formula = None if parsed_date else time_window

                    deadline = Deadline(
                        id=uuid.uuid4(),
                        contract_id=contract_id,
                        analysis_id=analysis_id,
                        user_id=user_id,
                        deadline_type=DeadlineType.OBLIGATION,
                        title=action[:200],
                        description=obligation.get('consequence'),
                        date=parsed_date,
                        date_formula=date_formula,
                        is_recurring=is_recurring(date_formula or ""),
                        is_completed=False,
                        source_section='obligations',
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )

                    db.add(deadline)
                    deadlines.append(deadline)

        # Extract from payment terms
        payment_terms = analysis_result.get('payment_terms', {})
        if isinstance(payment_terms, dict):
            # First due date
            first_due = payment_terms.get('first_due_date')
            if first_due:
                parsed_date = parse_date(first_due)
                if parsed_date:
                    deadline = Deadline(
                        id=uuid.uuid4(),
                        contract_id=contract_id,
                        analysis_id=analysis_id,
                        user_id=user_id,
                        deadline_type=DeadlineType.PAYMENT,
                        title=f"First payment due: {payment_terms.get('main_amount', 'Payment')}",
                        date=parsed_date,
                        is_recurring=False,
                        is_completed=False,
                        source_section='payment_terms',
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.add(deadline)
                    deadlines.append(deadline)

            # Recurring payments
            schedule = payment_terms.get('schedule') or payment_terms.get('frequency')
            if schedule and schedule.lower() not in ['one-time', 'none']:
                deadline = Deadline(
                    id=uuid.uuid4(),
                    contract_id=contract_id,
                    analysis_id=analysis_id,
                    user_id=user_id,
                    deadline_type=DeadlineType.PAYMENT,
                    title=f"Recurring payment: {payment_terms.get('main_amount', 'Payment')}",
                    date_formula=schedule,
                    is_recurring=True,
                    is_completed=False,
                    source_section='payment_terms',
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(deadline)
                deadlines.append(deadline)

        db.commit()
        logger.info(f"Extracted {len(deadlines)} deadlines from analysis {analysis_id}")

    except Exception as e:
        logger.error(f"Error extracting deadlines: {e}", exc_info=True)
        db.rollback()

    return deadlines


def get_upcoming_deadlines(
    user_id: uuid.UUID,
    days_ahead: int = 30,
    db: Session = None
) -> List[Deadline]:
    """
    Get upcoming deadlines for a user within the next N days

    Args:
        user_id: User UUID
        days_ahead: Number of days to look ahead (default 30)
        db: Database session

    Returns:
        List of Deadline objects
    """
    from datetime import timedelta

    cutoff_date = datetime.utcnow() + timedelta(days=days_ahead)

    deadlines = db.query(Deadline).filter(
        Deadline.user_id == user_id,
        Deadline.is_completed == False,
        Deadline.date != None,
        Deadline.date <= cutoff_date
    ).order_by(Deadline.date.asc()).all()

    return deadlines
