"""
Step 1: Preparation Analysis
Extracts metadata, detects document type, assesses quality
"""

import os
from typing import Dict, Any
from pathlib import Path
from .llm_router import LLMRouter
from .parsers import detect_structure
from .language import detect_governing_language, detect_jurisdiction, estimate_timezone
from .quality import compute_coverage_score


def load_prompt_template(language: str, prompt_type: str = "preparation") -> str:
    """
    Load prompt template for given language

    Args:
        language: Language code (english, russian, serbian, french)
        prompt_type: "preparation" or "analysis"

    Returns:
        Prompt template string
    """
    # For prototype, start with English only
    # Can add other languages later
    prompt_file = Path(__file__).parent / "prompts" / f"{prompt_type}_en.txt"

    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt template not found: {prompt_file}")

    return prompt_file.read_text()


def extract_referenced_documents(text: str) -> list:
    """
    Extract references to other documents (exhibits, annexes, schedules)

    Args:
        text: Contract text

    Returns:
        List of referenced document names
    """
    import re

    patterns = [
        r'Exhibit\s+([A-Z0-9]+)',
        r'Annex\s+([A-Z0-9]+)',
        r'Schedule\s+([A-Z0-9]+)',
        r'Appendix\s+([A-Z0-9]+)',
        r'Приложение\s+([А-Я0-9]+)',  # Russian
        r'Prilог\s+([A-Z0-9]+)',  # Serbian
        r'Annexe\s+([A-Z0-9]+)',  # French
    ]

    referenced = set()
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        referenced.update(matches)

    return list(referenced)


def run_step1_preparation(
    contract_text: str,
    detected_language: str,
    quality_score: float,
    llm_router: LLMRouter
) -> Dict[str, Any]:
    """
    Run Step 1: Preparation analysis

    Args:
        contract_text: Extracted contract text
        detected_language: Detected language from language detection
        quality_score: Quality score from document parser
        llm_router: LLM router instance

    Returns:
        Dictionary with Step 1 analysis results
    """
    # Load prompt template
    prompt_template = load_prompt_template(detected_language, "preparation")

    # Fill in the contract text
    prompt = prompt_template.replace("{contract_text}", contract_text[:15000])  # Limit to ~15k chars

    # Call LLM
    try:
        result = llm_router.call_with_json(
            prompt=prompt,
            system_prompt="You are a legal document analyst. Extract information accurately and return valid JSON."
        )
    except Exception as e:
        raise RuntimeError(f"Step 1 analysis failed: {str(e)}")

    # Detect document structure
    structure = detect_structure(contract_text)

    # Detect governing language info
    gov_lang_info = detect_governing_language(contract_text, detected_language)

    # Detect jurisdiction
    jurisdiction = detect_jurisdiction(contract_text)
    timezone = estimate_timezone(jurisdiction)

    # Extract referenced documents
    referenced_docs = extract_referenced_documents(contract_text)

    # Compute coverage (for prototype testing, assume annexes are not critical)
    # In production, this would check if referenced documents were uploaded
    coverage = 1.0 if len(referenced_docs) <= 5 else 0.5  # Don't penalize reasonable annex references

    # Merge all data
    preparation_data = {
        **result,  # LLM extraction
        "detected_language": detected_language,
        "has_headings": structure["has_headings"],
        "appears_complete": structure["appears_complete"],
        "is_translation": gov_lang_info["is_translation"],
        "has_original_attached": gov_lang_info["has_original_attached"],
        "governing_language_notes": gov_lang_info["notes"],
        "detected_jurisdiction": jurisdiction,
        "timezone_hint": timezone or result.get("timezone_hint"),
        "coverage_score": coverage,
        "quality_score": quality_score,
        "structure_sections": structure.get("sections", [])
    }

    return preparation_data


def assess_negotiability_from_text(text: str, agreement_type: str) -> tuple:
    """
    Simple heuristic-based negotiability assessment

    Args:
        text: Contract text
        agreement_type: Type of agreement

    Returns:
        tuple of (negotiability_level, reason)
    """
    text_lower = text.lower()

    # Low negotiability indicators
    low_indicators = [
        "terms of service",
        "by clicking",
        "by accessing",
        "you agree to",
        "these terms are binding",
        "non-negotiable"
    ]

    # High negotiability indicators
    high_indicators = [
        "parties agree to negotiate",
        "subject to negotiation",
        "to be mutually agreed",
        "draft for discussion"
    ]

    low_count = sum(1 for ind in low_indicators if ind in text_lower)
    high_count = sum(1 for ind in high_indicators if ind in text_lower)

    if low_count > high_count and low_count >= 2:
        return "low", "Take-it-or-leave-it terms (likely click-wrap or big provider)"
    elif high_count > low_count:
        return "high", "Open negotiation likely (draft or mutual agreement)"
    else:
        return "medium", "Some terms likely negotiable (standard business contract)"
