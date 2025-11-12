"""
Quality and confidence scoring for contract analysis
"""

from typing import Dict, Tuple
from .constants import QUALITY_FACTORS, CONFIDENCE_THRESHOLDS, HARD_GATES


def compute_quality_score(
    scan_quality: float,
    is_scanned: bool,
    is_translation: bool,
    has_original: bool,
    coverage: float,
    appears_complete: bool
) -> Tuple[float, str]:
    """
    Compute overall quality score for the document

    Args:
        scan_quality: 0-1 from PDF extraction
        is_scanned: whether document is scanned
        is_translation: whether document is translated
        has_original: whether original is attached/available
        coverage: 0-1 (proportion of referenced documents present)
        appears_complete: whether document has all typical sections

    Returns:
        tuple of (quality_score, reason_string)
    """
    score = 1.0
    reasons = []

    # Factor 1: Scan quality
    if scan_quality < 0.6:
        score *= QUALITY_FACTORS["poor_scan"]
        reasons.append("poor scan quality")
    elif is_scanned:
        score *= QUALITY_FACTORS["ocr_used"]
        reasons.append("OCR-extracted text")

    # Factor 2: Translation
    if is_translation and not has_original:
        score *= QUALITY_FACTORS["translation_without_original"]
        reasons.append("translation without original")

    # Factor 3: Coverage (missing annexes)
    if coverage < 1.0:
        score *= (0.8 + 0.2 * coverage)  # Scale between 0.8 and 1.0
        missing_pct = int((1 - coverage) * 100)
        reasons.append(f"{missing_pct}% of referenced documents missing")

    # Factor 4: Completeness
    if not appears_complete:
        score *= QUALITY_FACTORS["partial_document"]
        reasons.append("document appears incomplete")

    reason = "; ".join(reasons) if reasons else "complete, clean document"

    return score, reason


def compute_confidence_level(quality_score: float) -> Tuple[str, bool]:
    """
    Map quality score to confidence level

    Args:
        quality_score: 0-1 quality score

    Returns:
        tuple of (confidence_level_string, should_proceed_with_full_analysis)
    """
    if quality_score >= CONFIDENCE_THRESHOLDS["high"]:
        return "High", True
    elif quality_score >= CONFIDENCE_THRESHOLDS["medium"]:
        return "Medium", True
    else:
        return "Low", False  # Auto-downgrade to preliminary review


def check_hard_gates(scan_quality: float, coverage: float) -> Tuple[bool, str]:
    """
    Check if document passes hard gates for analysis

    Args:
        scan_quality: 0-1 scan quality
        coverage: 0-1 coverage score

    Returns:
        tuple of (can_proceed, reason_if_stopped)
    """
    if scan_quality < HARD_GATES["scan_legibility"]:
        return False, f"Scan too poor to read reliably (quality: {scan_quality:.1%})"

    if coverage < HARD_GATES["coverage"]:
        missing_pct = int((1 - coverage) * 100)
        return False, f"More than half of referenced documents missing ({missing_pct}%)"

    return True, ""


def compute_coverage_score(referenced_docs: list, available_docs: list) -> float:
    """
    Compute coverage score based on available vs referenced documents

    Args:
        referenced_docs: list of document names mentioned in contract
        available_docs: list of documents actually uploaded

    Returns:
        coverage score 0-1
    """
    if not referenced_docs:
        return 1.0  # No documents referenced, so 100% coverage

    # Match available docs to referenced (case-insensitive, partial match)
    available_lower = [doc.lower() for doc in available_docs]
    matched = 0

    for ref_doc in referenced_docs:
        ref_lower = ref_doc.lower()
        # Check if any available doc contains the reference (or vice versa)
        if any(ref_lower in avail or avail in ref_lower for avail in available_lower):
            matched += 1

    return matched / len(referenced_docs)


def build_confidence_explanation(
    confidence_level: str,
    quality_reason: str,
    coverage: float,
    num_files: int
) -> str:
    """
    Build human-readable confidence explanation

    Args:
        confidence_level: "High", "Medium", or "Low"
        quality_reason: reason string from quality computation
        coverage: coverage score 0-1
        num_files: number of files analyzed

    Returns:
        formatted confidence explanation string
    """
    file_text = f"{num_files} document{'s' if num_files != 1 else ''}"

    if coverage < 1.0:
        missing_count = int((1 - coverage) * 10)  # Rough estimate
        coverage_text = f"missing {missing_count}+ referenced documents"
    else:
        coverage_text = "all referenced documents present"

    explanation = f"Reviewed {file_text}; {coverage_text}. {quality_reason.capitalize()}."

    return explanation
