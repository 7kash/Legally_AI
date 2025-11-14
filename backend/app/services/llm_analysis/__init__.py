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
    compute_coverage_score,
    build_confidence_explanation
)
from .llm_router import LLMRouter
from .step1_preparation import run_step1_preparation
from .step2_analysis import run_step2_analysis
from .formatter import format_analysis_output, format_error_output

__all__ = [
    # Constants
    'LANGUAGES',
    'SCREENING_RESULTS',
    'IMPORTANT_LIMITS',
    'UI_STRINGS',

    # Parsers
    'extract_text',
    'detect_structure',

    # Language
    'detect_language',
    'detect_governing_language',
    'detect_jurisdiction',

    # Quality
    'compute_quality_score',
    'compute_confidence_level',
    'check_hard_gates',
    'compute_coverage_score',
    'build_confidence_explanation',

    # LLM
    'LLMRouter',

    # Analysis
    'run_step1_preparation',
    'run_step2_analysis',

    # Formatter
    'format_analysis_output',
    'format_error_output'
]
