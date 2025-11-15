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
) -> str:
    """
    Format complete analysis output for display

    Args:
        preparation_data: Step 1 results
        analysis_data: Step 2 results
        output_language: Language for output (english, russian, serbian, french)

    Returns:
        Formatted markdown string for Gradio display
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

    # Build output
    output = f"""
# {strings['summary_title']}

## {strings['our_quick_take']}

**{screening_text}**

---

## {strings['important_limits_title']}

{IMPORTANT_LIMITS[output_language]}

---

## {strings['confidence_title']}

**{strings[f'confidence_{confidence_level.lower()}']}** — {confidence_explanation}

---

# {strings['about_contract']}

{generate_about_section(preparation_data, analysis_data)}

---

## {strings['payment_title']}

"""

    # Add payment bullets
    payment_bullets = generate_payment_section(analysis_data, preparation_data)
    for bullet in payment_bullets:
        output += f"- {bullet}\n"

    output += "\n---\n\n"
    output += f"## {strings['obligations_title']}\n\n"

    # Add obligation bullets
    obligation_bullets = generate_obligations_section(analysis_data)
    for bullet in obligation_bullets:
        output += f"- {bullet}\n"

    output += "\n---\n\n"
    output += f"## {strings['check_terms']}\n\n"

    # Add risks as "terms to check"
    risks = analysis_data.get('risks', [])
    for risk in risks[:5]:
        output += f"- **{risk.get('description', '')}** — {risk.get('recommendation', '')}\n"

    if len(risks) > 5:
        output += f"\n*{strings['more_button']}* (showing top 5 of {len(risks)})\n"

    output += "\n---\n\n"
    output += f"## {strings['also_think']}\n\n"

    # Add gaps & anomalies as "also think about"
    gaps = analysis_data.get('gaps_anomalies', [])
    for gap in gaps[:5]:
        output += f"- {gap}\n"

    if len(gaps) > 5:
        output += f"\n*{strings['more_button']}* (showing top 5 of {len(gaps)})\n"

    output += "\n---\n\n"

    # Only show "Ask for these changes" if negotiability isn't low
    negotiability = preparation_data.get('negotiability', 'medium')
    if negotiability != 'low':
        output += f"## {strings['ask_changes']}\n\n"
        suggestions = analysis_data.get('suggestions', [])
        if suggestions:
            for suggestion in suggestions[:5]:
                output += f"- {suggestion}\n"
            if len(suggestions) > 5:
                output += f"\n*{strings['more_button']}* (showing top 5 of {len(suggestions)})\n"
        else:
            output += "*Based on the analysis, no specific changes to request were identified.*\n"
        output += "\n---\n\n"

    output += f"## {strings['sign_as_is']}\n\n"
    mitigations = analysis_data.get('mitigations', [])
    if mitigations:
        for mitigation in mitigations[:5]:
            output += f"- {mitigation}\n"
        if len(mitigations) > 5:
            output += f"\n*{strings['more_button']}* (showing top 5 of {len(mitigations)})\n"
    else:
        output += "*Based on the analysis, no specific mitigations were identified.*\n"
    output += "\n---\n\n"

    output += f"## {strings['act_now']}\n\n"

    # Add calendar items if any
    calendar = analysis_data.get('calendar', [])
    if calendar:
        output += "**Important dates:**\n\n"
        for item in calendar[:5]:
            date_str = item.get('date_or_formula', '')
            event_str = item.get('event', '')
            if date_str and event_str:
                output += f"- **{date_str}**: {event_str}\n"
        if len(calendar) > 5:
            output += f"\n*{strings.get('more_button', 'More available')}* (showing top 5 of {len(calendar)})\n"
        output += "\n"
    else:
        output += "*No specific deadline dates were identified in this contract.*\n\n"

    output += "*Feature coming soon: Export to calendar, checklists, email templates*\n\n"
    output += "---\n\n"

    output += f"## {strings['all_terms']} (collapsed)\n\n"
    output += "<details>\n<summary>Click to expand all key terms</summary>\n\n"

    # Add extracted fields
    output += "### Extracted Fields\n\n"
    parties = preparation_data.get('parties', [])
    for party in parties:
        output += f"- **{party.get('role', 'Party')}**: {party.get('name', 'Unknown')}\n"

    if preparation_data.get('term_start'):
        output += f"- **Term Start**: {preparation_data.get('term_start')}\n"
    if preparation_data.get('term_end'):
        output += f"- **Term End**: {preparation_data.get('term_end')}\n"
    if preparation_data.get('detected_jurisdiction'):
        output += f"- **Jurisdiction**: {preparation_data.get('detected_jurisdiction')}\n"

    output += "\n</details>\n\n"

    output += "---\n\n"
    output += "*This is a prototype. Feedback welcome!*\n"

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
