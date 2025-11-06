"""
Step 2: Text Analysis
Extracts obligations, rights, risks, and generates recommendations
"""

from typing import Dict, Any
from .llm_router import LLMRouter
from .step1_preparation import load_prompt_template


def run_step2_analysis(
    contract_text: str,
    preparation_data: Dict[str, Any],
    llm_router: LLMRouter
) -> Dict[str, Any]:
    """
    Run Step 2: Text Analysis

    Args:
        contract_text: Extracted contract text
        preparation_data: Results from Step 1
        llm_router: LLM router instance

    Returns:
        Dictionary with Step 2 analysis results
    """
    # Load prompt template
    prompt_template = load_prompt_template("english", "analysis")

    # Prepare preparation data summary for context
    prep_summary = f"""
Agreement Type: {preparation_data.get('agreement_type', 'unknown')}
User Role: {preparation_data.get('user_role', 'unknown')}
Negotiability: {preparation_data.get('negotiability', 'medium')}
Jurisdiction: {preparation_data.get('detected_jurisdiction', 'unknown')}
Quality Score: {preparation_data.get('quality_score', 0.5):.2f}
Coverage: {preparation_data.get('coverage_score', 1.0):.2f}
"""

    # Fill in the template
    prompt = prompt_template.replace("{preparation_data}", prep_summary)
    prompt = prompt.replace("{contract_text}", contract_text[:15000])  # Limit to ~15k chars
    prompt = prompt.replace("{user_role}", preparation_data.get('user_role', 'user'))
    prompt = prompt.replace("{agreement_type}", preparation_data.get('agreement_type', 'agreement'))

    # Call LLM
    try:
        result = llm_router.call_with_json(
            prompt=prompt,
            system_prompt="You are a legal document analyst helping non-lawyers understand contracts. Be clear, specific, and actionable."
        )
    except Exception as e:
        raise RuntimeError(f"Step 2 analysis failed: {str(e)}")

    # Add metadata
    analysis_data = {
        **result,
        "agreement_type": preparation_data.get('agreement_type'),
        "user_role": preparation_data.get('user_role'),
        "negotiability": preparation_data.get('negotiability')
    }

    return analysis_data


def generate_about_section(preparation_data: Dict, analysis_data: Dict) -> str:
    """
    Generate "What this agreement is about" section (2-3 sentences, ≤300 chars)

    Args:
        preparation_data: Step 1 results
        analysis_data: Step 2 results

    Returns:
        About text
    """
    # Use LLM-generated summary if available
    if analysis_data.get('about_summary'):
        return analysis_data['about_summary'][:300]

    # Fallback to generated text
    parties = preparation_data.get('parties', [])
    agreement_type = preparation_data.get('agreement_type', 'agreement')
    user_role = preparation_data.get('user_role', 'party')

    # Try to get party names
    party_names = [p.get('name', '') for p in parties if p.get('name')]

    if len(party_names) >= 2:
        parties_text = f"between {party_names[0]} and {party_names[1]}"
    else:
        parties_text = "between the parties"

    term_start = preparation_data.get('term_start')
    term_end = preparation_data.get('term_end')

    if term_start and term_end:
        term_text = f"from {term_start} to {term_end}"
    else:
        term_text = ""

    about = f"This is a {agreement_type} {parties_text}. "
    about += f"You are the {user_role}. "

    if term_text:
        about += f"The agreement runs {term_text}."

    # Truncate to 300 chars
    if len(about) > 300:
        about = about[:297] + "..."

    return about


def generate_payment_section(analysis_data: Dict, preparation_data: Dict = None) -> list:
    """
    Generate "What you pay and when" section (up to 5 bullets, ≤120 chars each)

    Args:
        analysis_data: Step 2 results (contains payment_terms)
        preparation_data: Step 1 results (fallback)

    Returns:
        List of payment bullet points
    """
    bullets = []

    # Use LLM-generated payment terms if available
    payment_terms = analysis_data.get('payment_terms', {})

    if payment_terms.get('main_amount'):
        bullets.append(f"Amount: {payment_terms['main_amount']}"[:120])

    if payment_terms.get('deposit_upfront'):
        bullets.append(f"Deposit: {payment_terms['deposit_upfront']}"[:120])

    if payment_terms.get('first_due_date'):
        bullets.append(f"First due: {payment_terms['first_due_date']}"[:120])

    if payment_terms.get('due_frequency'):
        bullets.append(f"Frequency: {payment_terms['due_frequency']}"[:120])

    if payment_terms.get('end_date_renewal'):
        bullets.append(f"Term: {payment_terms['end_date_renewal']}"[:120])

    if payment_terms.get('cancellation_notice'):
        bullets.append(f"To cancel: {payment_terms['cancellation_notice']}"[:120])

    # Always add taxes note
    bullets.append(payment_terms.get('taxes_fees_note', 'Taxes/fees not analyzed.'))

    # Fallback if no LLM payment terms
    if not bullets and preparation_data:
        key_amounts = preparation_data.get('key_amounts', [])
        if key_amounts:
            amounts_text = ", ".join([str(a.get('amount', a)) if isinstance(a, dict) else str(a) for a in key_amounts[:3]])
            bullets.append(f"Amounts: {amounts_text}"[:120])

        term_start = preparation_data.get('term_start')
        if term_start:
            bullets.append(f"First payment: {term_start}"[:120])

        bullets.append("Taxes/fees not analyzed.")

    return bullets[:5]


def generate_obligations_section(analysis_data: Dict) -> list:
    """
    Generate "What you agree to do" section (up to 5 bullets, ≤120 chars each)

    Args:
        analysis_data: Step 2 results

    Returns:
        List of obligation bullet points
    """
    obligations = analysis_data.get('obligations', [])

    bullets = []
    for obl in obligations[:5]:
        action = obl.get('action', '')
        time_window = obl.get('time_window', '')

        if time_window:
            bullet = f"{action} ({time_window})"
        else:
            bullet = action

        bullets.append(bullet[:120])

    return bullets


def determine_final_screening_result(
    analysis_screening: str,
    quality_score: float,
    coverage_score: float
) -> str:
    """
    Determine final screening result considering quality

    Args:
        analysis_screening: Screening result from Step 2 LLM
        quality_score: Quality score 0-1
        coverage_score: Coverage score 0-1

    Returns:
        Final screening result (one of 4 variants)
    """
    # If quality too low, force preliminary_review
    if quality_score < 0.5 or coverage_score < 0.5:
        return "preliminary_review"

    # Otherwise use LLM's assessment
    return analysis_screening
