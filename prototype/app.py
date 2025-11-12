"""
Legally AI - Contract Analysis Prototype
Main Gradio application for Hugging Face Spaces
"""

import gradio as gr
import os
from pathlib import Path
import tempfile

# Import our modules
from src.parsers import extract_text
from src.language import detect_language
from src.quality import (
    compute_quality_score,
    compute_confidence_level,
    check_hard_gates
)
from src.llm_router import LLMRouter
from src.step1_preparation import run_step1_preparation
from src.step2_analysis import run_step2_analysis
from src.formatter import format_analysis_output, format_error_output, format_loading_message
from src.constants import LANGUAGES, UI_STRINGS


# Initialize LLM router
try:
    # Get provider from environment variable (defaults to "groq")
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    llm_router = LLMRouter(provider=provider)
    print(f"LLM Router initialized with provider: {provider}")
except Exception as e:
    print(f"Warning: Could not initialize LLM router: {e}")
    print("Make sure the appropriate API key is set (GROQ_API_KEY or DEEPSEEK_API_KEY)")
    llm_router = None


def analyze_contract(file, output_language):
    """
    Main analysis function called by Gradio

    Args:
        file: Uploaded file object
        output_language: Selected output language

    Yields:
        Progress updates (markdown strings)
    """
    if llm_router is None:
        yield format_error_output(
            "LLM router not initialized. Please set GROQ_API_KEY environment variable.",
            output_language
        )
        return

    if file is None:
        yield format_error_output("Please upload a contract file (PDF or DOCX).", output_language)
        return

    try:
        # Stage 1: Parse document
        yield format_loading_message("parsing", output_language)

        file_path = file.name
        extraction = extract_text(file_path)

        text = extraction['text']
        quality_score_raw = extraction['quality_score']
        is_scanned = extraction['is_scanned']

        if not text or len(text) < 100:
            yield format_error_output(
                "Document appears to be empty or too short. Please upload a valid contract.",
                output_language
            )
            return

        # Stage 2: Detect language
        yield format_loading_message("language", output_language)

        detected_lang, lang_confidence = detect_language(text)

        # Stage 3: Run Step 1 (Preparation)
        yield format_loading_message("preparation", output_language)

        preparation_data = run_step1_preparation(
            contract_text=text,
            detected_language=detected_lang,
            quality_score=quality_score_raw,
            llm_router=llm_router
        )

        # Check hard gates
        can_proceed, gate_reason = check_hard_gates(
            quality_score_raw,
            preparation_data.get('coverage_score', 1.0)
        )

        if not can_proceed:
            # Return preliminary review
            yield format_error_output(
                f"Cannot reliably analyze this document: {gate_reason}\n\n"
                "Please provide a clean, complete copy with all annexes and try again.",
                output_language
            )
            return

        # Compute final quality and confidence
        quality_score, quality_reason = compute_quality_score(
            scan_quality=quality_score_raw,
            is_scanned=is_scanned,
            is_translation=preparation_data.get('is_translation', False),
            has_original=preparation_data.get('has_original_attached', False),
            coverage=preparation_data.get('coverage_score', 1.0),
            appears_complete=preparation_data.get('appears_complete', True)
        )

        confidence_level, should_proceed = compute_confidence_level(quality_score)

        # Update preparation data
        preparation_data['quality_score'] = quality_score
        preparation_data['quality_reason'] = quality_reason
        preparation_data['confidence_level'] = confidence_level

        if not should_proceed:
            # Force preliminary review due to low confidence
            yield format_error_output(
                f"Low confidence ({confidence_level}): {quality_reason}\n\n"
                "We recommend providing a better quality document for reliable analysis.",
                output_language
            )
            return

        # Stage 4: Run Step 2 (Analysis)
        yield format_loading_message("analysis", output_language)

        analysis_data = run_step2_analysis(
            contract_text=text,
            preparation_data=preparation_data,
            llm_router=llm_router
        )

        # Stage 5: Format output
        yield format_loading_message("formatting", output_language)

        formatted_output = format_analysis_output(
            preparation_data=preparation_data,
            analysis_data=analysis_data,
            output_language=output_language
        )

        yield formatted_output

    except Exception as e:
        import traceback
        error_details = f"{str(e)}\n\n```\n{traceback.format_exc()}\n```"
        yield format_error_output(
            f"An error occurred during analysis:\n\n{error_details}",
            output_language
        )


# Build Gradio interface
def build_interface():
    """
    Build Gradio interface
    """
    with gr.Blocks(
        title="Legally AI - Contract Analysis",
        theme=gr.themes.Soft()
    ) as demo:

        gr.Markdown("""
        # 📜 Legally AI - Contract Analysis

        Upload your contract in **Russian, Serbian, French, or English** for AI-powered analysis.

        **⚠️ Disclaimer:** This is a prototype for testing. Not legal advice.
        """)

        with gr.Row():
            with gr.Column(scale=1):
                file_input = gr.File(
                    label="Upload Contract (PDF or DOCX)",
                    file_types=[".pdf", ".docx"],
                    type="filepath"
                )

                output_lang = gr.Radio(
                    choices=list(LANGUAGES.keys()),
                    label="Show results in:",
                    value="english"
                )

                analyze_btn = gr.Button(
                    "Analyze Contract",
                    variant="primary",
                    size="lg"
                )

                gr.Markdown("""
                ### How to use:
                1. Upload your contract (PDF or DOCX)
                2. Choose output language
                3. Click "Analyze Contract"
                4. Review the analysis (takes ~20-30 seconds)
                """)

            with gr.Column(scale=2):
                output = gr.Markdown(
                    label="Analysis Results",
                    value="Upload a contract to get started."
                )

        # Wire up the button
        analyze_btn.click(
            fn=analyze_contract,
            inputs=[file_input, output_lang],
            outputs=output,
            show_progress=True
        )

        gr.Markdown("""
        ---

        ### For testers:

        Please evaluate:
        - ✅ **Accuracy**: Are extracted terms correct?
        - ✅ **Completeness**: Are all important obligations/rights listed?
        - ✅ **Risks**: Are risk flags relevant and prioritized correctly?
        - ✅ **Translation** (if applicable): Is the translation quality good?
        - ❌ **Issues**: What's missing or incorrect?

        ### Important Limits

        This is an AI-powered informational screening — **not legal advice**, not a law-firm review,
        and it does not create an attorney–client relationship. We looked only at the text you provided
        and did not verify facts, identities, authority to sign, ownership, required formalities, or
        compliance with local law. Attachments, the governing-language version, or later edits can change
        the result. Laws differ by country and state, so enforceability may vary. Don't rely on this
        summary alone; for meaningful stakes, read everything and consider speaking with a qualified lawyer.

        ---

        **Technology**: Groq (llama-3.3-70b-versatile) / DeepSeek (deepseek-chat) · pdfplumber · Gradio

        **Version**: Prototype 0.1 (HF Spaces)
        """)

    return demo


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Build and launch
    demo = build_interface()
    demo.launch(
        share=False,  # Set to True if you want a public link
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860  # Default Gradio port
    )
