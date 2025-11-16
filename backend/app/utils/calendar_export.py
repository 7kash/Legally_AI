"""
Calendar export utilities
Generate .ics files from deadlines
"""

from typing import List
from datetime import datetime
from ..models import Deadline


def create_ics_from_deadline(deadline: Deadline) -> str:
    """
    Create .ics calendar content from a single deadline

    Args:
        deadline: Deadline object

    Returns:
        .ics file content as string
    """
    if not deadline.date:
        raise ValueError("Deadline must have a date to export")

    # Format datetime for iCal
    dt_start = deadline.date.strftime("%Y%m%dT%H%M%SZ")
    dt_now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Build description
    description = deadline.description or deadline.title
    if deadline.source_section:
        description += f"\\n\\nSource: {deadline.source_section}"

    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Legally AI//Contract Deadlines//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{deadline.id}@legally-ai.com
DTSTAMP:{dt_now}
DTSTART:{dt_start}
SUMMARY:{deadline.title}
DESCRIPTION:{description}
STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
END:VCALENDAR"""

    return ics_content


def create_ics_from_deadlines(deadlines: List[Deadline]) -> str:
    """
    Create .ics calendar content from multiple deadlines

    Args:
        deadlines: List of Deadline objects

    Returns:
        .ics file content as string
    """
    dt_now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # Start calendar
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Legally AI//Contract Deadlines//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]

    # Add each deadline as an event
    for deadline in deadlines:
        if not deadline.date:
            continue

        dt_start = deadline.date.strftime("%Y%m%dT%H%M%SZ")

        # Build description
        description = deadline.description or deadline.title
        if deadline.source_section:
            description += f"\\n\\nSource: {deadline.source_section}"

        # Escape commas and newlines in text fields
        title = deadline.title.replace(",", "\\,").replace("\n", "\\n")
        description = description.replace(",", "\\,").replace("\n", "\\n")

        ics_lines.extend([
            "BEGIN:VEVENT",
            f"UID:{deadline.id}@legally-ai.com",
            f"DTSTAMP:{dt_now}",
            f"DTSTART:{dt_start}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{description}",
            "STATUS:CONFIRMED",
            "SEQUENCE:0",
            "END:VEVENT"
        ])

    # End calendar
    ics_lines.append("END:VCALENDAR")

    return "\n".join(ics_lines)
