"""
ELI5 (Explain Like I'm 5) Simplification Service
Simplifies legal language into everyday terms using LLM
"""

from typing import Dict, Any, List, Optional
from .llm_router import LLMRouter
import logging

logger = logging.getLogger(__name__)


ELI5_PROMPT_TEMPLATE = """**Your Task:**
Rephrase the following contract analysis text in simple, everyday language that anyone can understand.

**Rules:**
1. REPHRASE the exact text provided below - do NOT create new content or add information
2. NO legal jargon, NO Latin terms, NO complex words
3. Use everyday words: "end" not "terminate", "pay" not "remuneration"
4. Keep sentences SHORT: Maximum 15 words per sentence
5. Add simple examples when helpful (e.g., "like when you...")
6. Use analogies to everyday situations
7. Be conversational and friendly
8. Keep the SAME meaning, just simpler words
9. Do NOT skip important details
10. Do NOT add ANY prefixes or introductions - start directly with the rephrased content
11. Put each section on a new line for better readability

**Example:**
Original: "What you can do: Terminate agreement
How to do it: Provide 30 days written notice
Any conditions: Must not be in breach"

Simplified:
What you can do:
You can end this agreement anytime.

How to do it:
Send a letter saying you want to end it. Do this 30 days before you want it to end.

Any conditions:
You can only do this if you haven't broken any rules in the agreement.

**Text to Rephrase:**
{text_to_simplify}"""


def simplify_text(text: str, llm_router: LLMRouter) -> str:
    """
    Simplify complex legal text using LLM

    Args:
        text: Original text to simplify
        llm_router: LLM router instance

    Returns:
        Simplified text in everyday language
    """
    if not text or len(text.strip()) == 0:
        return text

    try:
        prompt = ELI5_PROMPT_TEMPLATE.replace("{text_to_simplify}", text)

        simplified = llm_router.call(
            prompt=prompt,
            system_prompt="You are a helpful lawyer who explains complex legal concepts in simple, everyday language that anyone can understand.",
            temperature=0.1,  # Low temperature for consistent, accurate rephrasing
            max_tokens=1000
        )

        # Strip common prefixes that LLMs add despite instructions
        prefixes_to_remove = [
            "Here's the contract summary in simple, everyday language:",
            "Here is the contract summary in simple, everyday language:",
            "Here's the contract summary in simple language:",
            "Here is the contract summary in simple language:",
            "Here's the simplified contract summary:",
            "Here is the simplified contract summary:",
            "Here's the rephrased text:",
            "Here's the simplified version:",
            "Here is the rephrased text:",
            "Here is the simplified version:",
            "Rephrased:",
            "Simplified:",
            "In simple terms:",
            "In everyday language:",
        ]

        result = simplified.strip()

        # Try removing prefixes (case-insensitive check)
        for prefix in prefixes_to_remove:
            if result.lower().startswith(prefix.lower()):
                result = result[len(prefix):].strip()
                break

        return result

    except Exception as e:
        logger.error(f"ELI5 simplification failed: {e}", exc_info=True)
        # Return original text if simplification fails
        return text


def simplify_obligation(obligation: Dict[str, Any], llm_router: LLMRouter) -> Dict[str, Any]:
    """
    Simplify an obligation item

    Args:
        obligation: Obligation dictionary
        llm_router: LLM router instance

    Returns:
        Simplified obligation dictionary
    """
    simplified = obligation.copy()

    # Combine all text into one block for better context
    original_text = f"""
What you must do: {obligation.get('action', '')}
When: {obligation.get('trigger', '')}
Deadline: {obligation.get('time_window', '')}
What happens if you don't: {obligation.get('consequence', '')}
"""

    simplified_text = simplify_text(original_text, llm_router)

    # Store simplified version
    simplified['action_simple'] = simplified_text
    simplified['original_action'] = obligation.get('action', '')

    return simplified


def simplify_right(right: Dict[str, Any], llm_router: LLMRouter) -> Dict[str, Any]:
    """
    Simplify a rights item

    Args:
        right: Right dictionary
        llm_router: LLM router instance

    Returns:
        Simplified right dictionary
    """
    simplified = right.copy()

    original_text = f"""
What you can do: {right.get('right', '')}
How to do it: {right.get('how_to_exercise', '')}
Any conditions: {right.get('conditions', 'None')}
"""

    simplified_text = simplify_text(original_text, llm_router)

    simplified['right_simple'] = simplified_text
    simplified['original_right'] = right.get('right', '')

    return simplified


def simplify_risk(risk: Dict[str, Any], llm_router: LLMRouter) -> Dict[str, Any]:
    """
    Simplify a risk item

    Args:
        risk: Risk dictionary
        llm_router: LLM router instance

    Returns:
        Simplified risk dictionary
    """
    simplified = risk.copy()

    # Risk level in simple terms (emoji only)
    level_simple = {
        'high': '⚠️',
        'medium': '⚠️',
        'low': 'ℹ️'
    }.get(risk.get('level', 'medium').lower(), '⚠️')

    original_text = f"""
{level_simple}: {risk.get('description', '')}
What to do: {risk.get('recommendation', '')}
"""

    simplified_text = simplify_text(original_text, llm_router)

    simplified['description_simple'] = simplified_text
    simplified['original_description'] = risk.get('description', '')
    simplified['level_simple'] = level_simple

    return simplified


def simplify_mitigation(mitigation: Dict[str, Any], llm_router: LLMRouter) -> Dict[str, Any]:
    """
    Simplify a mitigation item

    Args:
        mitigation: Mitigation dictionary
        llm_router: LLM router instance

    Returns:
        Simplified mitigation dictionary
    """
    simplified = mitigation.copy()

    original_text = f"""
What to do to protect yourself: {mitigation.get('mitigation', '') or mitigation.get('action', '')}
Why this helps: {mitigation.get('rationale', '')}
When to do it: {mitigation.get('when', '')}
"""

    simplified_text = simplify_text(original_text, llm_router)

    simplified['mitigation_simple'] = simplified_text
    simplified['original_mitigation'] = mitigation.get('mitigation', '') or mitigation.get('action', '')

    return simplified


def simplify_analysis_section(
    section_name: str,
    section_data: List[Dict[str, Any]],
    llm_router: LLMRouter
) -> List[Dict[str, Any]]:
    """
    Simplify an entire analysis section (obligations, rights, risks, or mitigations)

    Args:
        section_name: Name of section ('obligations', 'rights', 'risks', 'mitigations')
        section_data: List of items in the section
        llm_router: LLM router instance

    Returns:
        List of simplified items
    """
    simplified_items = []

    for item in section_data:
        if not isinstance(item, dict):
            simplified_items.append(item)
            continue

        try:
            if section_name == 'obligations':
                simplified_item = simplify_obligation(item, llm_router)
            elif section_name == 'rights':
                simplified_item = simplify_right(item, llm_router)
            elif section_name == 'risks':
                simplified_item = simplify_risk(item, llm_router)
            elif section_name == 'mitigations':
                simplified_item = simplify_mitigation(item, llm_router)
            else:
                simplified_item = item

            simplified_items.append(simplified_item)

        except Exception as e:
            logger.error(f"Failed to simplify {section_name} item: {e}")
            simplified_items.append(item)  # Keep original on error

    return simplified_items


def simplify_about_summary(about_text: str, llm_router: LLMRouter) -> str:
    """
    Simplify the "About the Contract" summary text

    Args:
        about_text: Original about summary text
        llm_router: LLM router instance

    Returns:
        Simplified about summary in everyday language
    """
    if not about_text or len(about_text.strip()) == 0:
        return about_text

    try:
        # Use simplified prompt specifically for contract summaries
        prompt = f"""Rephrase this contract summary in simple, everyday language that anyone can understand.

**Rules:**
1. Use simple, everyday words - NO legal jargon
2. Keep sentences SHORT: Maximum 15 words per sentence
3. Be conversational and friendly
4. Keep the SAME meaning and key facts
5. Do NOT add ANY prefixes - start directly with the rephrased content

**Contract Summary to Rephrase:**
{about_text}"""

        simplified = llm_router.call(
            prompt=prompt,
            system_prompt="You are a helpful lawyer who explains complex legal concepts in simple, everyday language.",
            temperature=0.1,
            max_tokens=500
        )

        # Strip common prefixes that LLMs add despite instructions
        prefixes_to_remove = [
            "Here's the contract summary in simple, everyday language:",
            "Here is the contract summary in simple, everyday language:",
            "Here's the contract summary in simple language:",
            "Here is the contract summary in simple language:",
            "Here's the simplified contract summary:",
            "Here is the simplified contract summary:",
            "Here's the rephrased text:",
            "Here's the simplified version:",
            "Here is the rephrased text:",
            "Here is the simplified version:",
            "Rephrased:",
            "Simplified:",
            "In simple terms:",
            "In everyday language:",
        ]

        result = simplified.strip()

        # Try removing prefixes (case-insensitive check)
        for prefix in prefixes_to_remove:
            if result.lower().startswith(prefix.lower()):
                result = result[len(prefix):].strip()
                break

        return result

    except Exception as e:
        logger.error(f"ELI5 about summary simplification failed: {e}", exc_info=True)
        return about_text


def simplify_full_analysis(
    analysis_result: Dict[str, Any],
    sections_to_simplify: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Simplify entire analysis result

    Args:
        analysis_result: Complete analysis results
        sections_to_simplify: List of sections to simplify (default: all)

    Returns:
        Analysis with simplified versions added
    """
    if sections_to_simplify is None:
        sections_to_simplify = ['obligations', 'rights', 'risks', 'mitigations', 'about_summary']

    llm_router = LLMRouter()
    simplified_analysis = analysis_result.copy()

    for section in sections_to_simplify:
        if section not in analysis_result:
            continue

        section_data = analysis_result[section]

        # Special handling for about_summary (string, not list)
        if section == 'about_summary':
            if isinstance(section_data, str):
                try:
                    simplified_analysis['about_summary_simplified'] = simplify_about_summary(
                        section_data,
                        llm_router
                    )
                    logger.info(f"Simplified about_summary text")
                except Exception as e:
                    logger.error(f"Failed to simplify about_summary: {e}", exc_info=True)
            else:
                logger.warning(f"about_summary is not a string: {type(section_data)}")
            continue

        # Handle nested {content: [...]} structure
        if isinstance(section_data, dict) and 'content' in section_data:
            section_data = section_data['content']

        # Now check if it's a list
        if isinstance(section_data, list):
            try:
                simplified_analysis[f'{section}_simplified'] = simplify_analysis_section(
                    section,
                    section_data,
                    llm_router
                )
                logger.info(f"Simplified {len(section_data)} items in {section}")
            except Exception as e:
                logger.error(f"Failed to simplify {section}: {e}", exc_info=True)
        else:
            logger.warning(f"Section {section} is not a list or doesn't have content: {type(section_data)}")

    return simplified_analysis
