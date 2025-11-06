"""
Language detection and translation utilities
"""

from langdetect import detect, DetectorFactory
from typing import Tuple, Optional
from .constants import LANG_CODES

# Set seed for consistent results
DetectorFactory.seed = 0


def detect_language(text: str) -> Tuple[str, float]:
    """
    Detect the language of the text

    Args:
        text: Text to analyze

    Returns:
        tuple of (language_name, confidence)
        e.g., ("russian", 0.9)
    """
    # Use first 2000 characters for detection (faster, usually sufficient)
    sample = text[:2000] if len(text) > 2000 else text

    try:
        # langdetect returns ISO 639-1 code (e.g., 'en', 'ru')
        code = detect(sample)

        # Map to our language names
        language = LANG_CODES.get(code, "english")  # Default to English if unknown

        # langdetect doesn't give confidence, so we estimate
        confidence = 0.9  # Assume high confidence if detection succeeds

        return language, confidence

    except Exception as e:
        # If detection fails, default to English with low confidence
        return "english", 0.5


def detect_governing_language(text: str, detected_lang: str) -> dict:
    """
    Detect if document is a translation or original

    Returns:
        dict with:
        - is_translation: boolean
        - governing_language: likely original language
        - has_original_attached: whether original mentioned/attached
        - notes: string with observations
    """
    notes = []

    # Check for translation indicators
    translation_indicators = {
        "english": ["translated from", "translation of", "original in"],
        "russian": ["перевод с", "оригинал на"],
        "serbian": ["prevod sa", "original na"],
        "french": ["traduit de", "original en"]
    }

    is_translation = False
    governing_language = detected_lang

    # Search for indicators
    for lang, indicators in translation_indicators.items():
        for indicator in indicators:
            if indicator.lower() in text.lower():
                is_translation = True
                notes.append(f"Translation indicator found: '{indicator}'")
                break

    # Check for "bilingual" or dual-language notes
    bilingual_indicators = [
        "bilingual", "двуязычный", "dwojezičn", "bilingue",
        "Serbian version prevails", "Русская версия имеет преимущественную силу"
    ]

    has_original_attached = False
    for indicator in bilingual_indicators:
        if indicator.lower() in text.lower():
            notes.append(f"Bilingual note found: '{indicator}'")
            # Try to determine which language prevails
            if "Serbian" in indicator or "Српски" in indicator:
                governing_language = "serbian"
            elif "Russian" in indicator or "Русский" in indicator:
                governing_language = "russian"

    # Check if original document is mentioned as attached
    attachment_indicators = ["attached hereto", "приложен", "priložen", "joint", "annex"]
    for indicator in attachment_indicators:
        if indicator.lower() in text.lower():
            has_original_attached = True
            notes.append("Reference to attached original found")

    return {
        "is_translation": is_translation,
        "governing_language": governing_language,
        "has_original_attached": has_original_attached,
        "notes": "; ".join(notes) if notes else "No translation indicators found"
    }


def detect_jurisdiction(text: str) -> Optional[str]:
    """
    Detect jurisdiction/governing law from text

    Returns:
        string with jurisdiction (e.g., "Serbia", "Russia", "France") or None
    """
    jurisdiction_patterns = {
        "Serbia": ["Serbia", "Serbian law", "Belgrade", "Србија", "српско право"],
        "Russia": ["Russia", "Russian Federation", "Moscow", "Россия", "российское право"],
        "France": ["France", "French law", "Paris", "droit français"],
        "United States": ["United States", "U.S.", "USA", "American law", "New York", "California"],
        "United Kingdom": ["United Kingdom", "UK", "England", "Wales", "English law"],
    }

    # Count mentions of each jurisdiction
    mentions = {}
    for jurisdiction, patterns in jurisdiction_patterns.items():
        count = sum(1 for pattern in patterns if pattern.lower() in text.lower())
        if count > 0:
            mentions[jurisdiction] = count

    # Return jurisdiction with most mentions
    if mentions:
        return max(mentions, key=mentions.get)

    return None


def estimate_timezone(jurisdiction: Optional[str]) -> Optional[str]:
    """
    Estimate timezone based on jurisdiction

    Args:
        jurisdiction: Detected jurisdiction

    Returns:
        Timezone string (e.g., "Europe/Belgrade") or None
    """
    timezone_map = {
        "Serbia": "Europe/Belgrade",
        "Russia": "Europe/Moscow",  # Simplified - Russia has many timezones
        "France": "Europe/Paris",
        "United States": "America/New_York",  # Simplified - US has many timezones
        "United Kingdom": "Europe/London"
    }

    return timezone_map.get(jurisdiction)
