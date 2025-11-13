"""
Output Formatter
Formats analysis results for UI display according to specification
"""

from typing import Dict, Any
from .constants import SCREENING_RESULTS, IMPORTANT_LIMITS, UI_STRINGS
from .quality import build_confidence_explanation
from .step2_analysis import (
    generate_about_section,
    generate_payment_section,
    generate_obligations_section,
    determine_final_screening_result
)


def format_analysis_output(
    preparation_data: Dict[str, Any],
    analysis_data: Dict[str, Any],
    output_language: str = "english"
) -> Dict[str, Any]:
    """
    Format complete analysis output for display

    Args:
        preparation_data: Step 1 results
        analysis_data: Step 2 results
        output_language: Language for output (english, russian, serbian, french)

    Returns:
        Structured dictionary for frontend display
    """
    strings = UI_STRINGS[output_language]

    # Determine final screening result
    screening_result = determine_final_screening_result(
        analysis_data.get('screening_result', 'recommended_to_address'),
        preparation_data.get('quality_score', 0.5),
        preparation_data.get('coverage_score', 1.0)
    )

    # Get screening result text
    screening_text = SCREENING_RESULTS[screening_result][output_language]

    # Build confidence explanation
    confidence_level = "High" if preparation_data.get('quality_score', 0) >= 0.8 else \
                      "Medium" if preparation_data.get('quality_score', 0) >= 0.5 else "Low"

    confidence_explanation = build_confidence_explanation(
        confidence_level,
        preparation_data.get('governing_language_notes', ''),
        preparation_data.get('coverage_score', 1.0),
        1  # Number of files
    )

    # Build structured output for frontend
    payment_bullets = generate_payment_section(analysis_data, preparation_data)
    obligation_bullets = generate_obligations_section(analysis_data)
    risks = analysis_data.get('risks', [])
    gaps = analysis_data.get('gaps_anomalies', [])
    calendar = analysis_data.get('calendar', [])
    parties = preparation_data.get('parties', [])
    negotiability = preparation_data.get('negotiability', 'medium')

    output = {
        "summary": {
            "title": strings['summary_title'],
            "quick_take": screening_text,
            "confidence": {
                "level": confidence_level,
                "explanation": confidence_explanation
            },
            "important_limits": IMPORTANT_LIMITS[output_language]
        },
        "about": {
            "title": strings['about_contract'],
            "content": generate_about_section(preparation_data, analysis_data)
        },
        "payment": {
            "title": strings['payment_title'],
            "items": payment_bullets
        },
        "obligations": {
            "title": strings['obligations_title'],
            "items": obligation_bullets
        },
        "risks": {
            "title": strings['check_terms'],
            "items": [
                {
                    "description": risk.get('description', ''),
                    "recommendation": risk.get('recommendation', '')
                }
                for risk in risks[:5]
            ],
            "total_count": len(risks)
        },
        "gaps_anomalies": {
            "title": strings['also_think'],
            "items": gaps[:5],
            "total_count": len(gaps)
        },
        "action_items": {
            "title": strings['act_now'],
            "calendar": calendar[:5] if calendar else []
        },
        "metadata": {
            "parties": parties,
            "term_start": preparation_data.get('term_start'),
            "term_end": preparation_data.get('term_end'),
            "jurisdiction": preparation_data.get('detected_jurisdiction'),
            "negotiability": negotiability
        }
    }

    return output


def format_error_output(error_message: str, output_language: str = "english") -> str:
    """
    Format error message for display

    Args:
        error_message: Error message
        output_language: Language for output

    Returns:
        Formatted error message
    """
    strings = UI_STRINGS[output_language]

    output = f"""
# ❌ Analysis Failed

{error_message}

## What you can try:

- Check that your file is a valid PDF or DOCX
- Make sure the file is not corrupted or password-protected
- Try with a different contract
- Contact us if the problem persists

---

{IMPORTANT_LIMITS[output_language]}
"""

    return output


def format_loading_message(stage: str, output_language: str = "english") -> str:
    """
    Format loading message for different stages

    Args:
        stage: Current stage (parsing, preparation, analysis, formatting)
        output_language: Language for output

    Returns:
        Loading message
    """
    strings = UI_STRINGS[output_language]

    stage_messages = {
        "english": {
            "parsing": "📄 Reading your document...",
            "language": "🌍 Detecting language...",
            "preparation": "🔍 Analyzing document structure...",
            "analysis": "🧠 Analyzing terms, obligations, and risks...",
            "formatting": "✨ Formatting results..."
        },
        "russian": {
            "parsing": "📄 Читаем ваш документ...",
            "language": "🌍 Определяем язык...",
            "preparation": "🔍 Анализируем структуру документа...",
            "analysis": "🧠 Анализируем условия, обязательства и риски...",
            "formatting": "✨ Форматируем результаты..."
        },
        "serbian": {
            "parsing": "📄 Čitamo vaš dokument...",
            "language": "🌍 Otkrivamo jezik...",
            "preparation": "🔍 Analiziramo strukturu dokumenta...",
            "analysis": "🧠 Analiziramo uslove, obaveze i rizike...",
            "formatting": "✨ Formatiramo rezultate..."
        },
        "french": {
            "parsing": "📄 Lecture de votre document...",
            "language": "🌍 Détection de la langue...",
            "preparation": "🔍 Analyse de la structure du document...",
            "analysis": "🧠 Analyse des conditions, obligations et risques...",
            "formatting": "✨ Formatage des résultats..."
        }
    }

    return stage_messages.get(output_language, stage_messages["english"]).get(stage, strings['analyzing'])
