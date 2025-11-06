"""
Legally AI - Contract Analysis Prototype
Source package initialization
"""

from .constants import *
from .parsers import extract_text, detect_structure
from .language import detect_language, detect_governing_language, detect_jurisdiction
from .quality import (
    compute_quality_score,
    compute_confidence_level,
    check_hard_gates,
    compute_coverage_score
)
from .llm_router import LLMRouter

__all__ = [
    'LANGUAGES',
    'SCREENING_RESULTS',
    'IMPORTANT_LIMITS',
    'UI_STRINGS',
    'extract_text',
    'detect_structure',
    'detect_language',
    'detect_governing_language',
    'detect_jurisdiction',
    'compute_quality_score',
    'compute_confidence_level',
    'check_hard_gates',
    'compute_coverage_score',
    'LLMRouter'
]
