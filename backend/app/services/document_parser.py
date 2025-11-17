"""
Document parser service for extracting text from PDF and DOCX files
Includes OCR support for scanned PDFs
"""

from pathlib import Path
from typing import Dict, Any
import pdfplumber
from docx import Document

# OCR support for scanned PDFs
try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


def extract_text_with_ocr(file_path: str) -> Dict[str, Any]:
    """
    Extract text from scanned PDF using OCR

    Args:
        file_path: Path to PDF file

    Returns:
        dict with extracted text and metadata
    """
    if not OCR_AVAILABLE:
        raise ValueError(
            "OCR libraries not available. Install with: pip install pdf2image pytesseract pillow"
        )

    try:
        # Convert PDF to images
        print(f"Converting PDF to images: {file_path}")
        images = convert_from_path(file_path)
        print(f"Converted {len(images)} pages to images")

        pages = []
        total_chars = 0

        for i, image in enumerate(images):
            # Perform OCR on each page with multi-language support
            # Try English first, then add other languages if available
            print(f"Processing page {i+1}/{len(images)} with OCR...")
            try:
                # Try with English only first (most reliable)
                text = pytesseract.image_to_string(image, lang='eng')
                print(f"Page {i+1} processed: {len(text)} characters extracted")
            except Exception as e:
                print(f"OCR failed on page {i+1}: {e}")
                text = ""

            if text.strip():
                pages.append(text)
                total_chars += len(text)

        full_text = "\n\n".join(pages)
        avg_chars_per_page = total_chars / len(images) if images else 0

        # OCR quality varies, estimate based on text extracted
        quality_score = min(0.8, avg_chars_per_page / 2000)  # Max 0.8 for OCR

        return {
            "text": full_text,
            "page_count": len(images),
            "has_text": len(full_text.strip()) > 0,
            "format": "pdf",
            "is_scanned": True,
            "quality_score": quality_score,
            "avg_chars_per_page": avg_chars_per_page
        }

    except Exception as e:
        raise ValueError(f"Failed to perform OCR on PDF: {str(e)}")


def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
    """
    Extract text from PDF file using pdfplumber
    Automatically uses OCR if document appears to be scanned

    Returns:
        dict with:
        - text: extracted text
        - page_count: number of pages
        - has_text: whether text was extracted
        - is_scanned: whether document appears to be scanned
        - quality_score: estimate of scan quality (0-1)
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            pages = []
            total_chars = 0

            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
                    total_chars += len(text)

            full_text = "\n\n".join(pages)

            # Estimate quality
            avg_chars_per_page = total_chars / len(pdf.pages) if pdf.pages else 0

            # Typical printed page has 2000-4000 chars
            # Less than 500 suggests poor OCR or scanned without OCR
            quality_score = min(1.0, avg_chars_per_page / 2000)
            is_scanned = avg_chars_per_page < 500

            # If document appears scanned (little/no text), try OCR
            if is_scanned and OCR_AVAILABLE and avg_chars_per_page < 200:
                print(f"PDF appears scanned (avg {avg_chars_per_page:.0f} chars/page), attempting OCR...")
                return extract_text_with_ocr(file_path)

            return {
                "text": full_text,
                "page_count": len(pdf.pages),
                "has_text": len(full_text.strip()) > 0,
                "format": "pdf",
                "is_scanned": is_scanned,
                "quality_score": quality_score,
                "avg_chars_per_page": avg_chars_per_page
            }

    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")


def extract_text_from_docx(file_path: str) -> Dict[str, Any]:
    """
    Extract text from DOCX file

    Returns:
        dict with:
        - text: extracted text
        - paragraph_count: number of paragraphs
        - has_text: whether text was extracted
        - quality_score: always 1.0 for DOCX (digital format)
    """
    try:
        doc = Document(file_path)

        paragraphs = []

        # Extract text from paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)

        # Extract text from tables
        for table in doc.tables:
            for row in table.rows:
                row_text = []
                for cell in row.cells:
                    if cell.text.strip():
                        row_text.append(cell.text.strip())
                if row_text:
                    paragraphs.append(" | ".join(row_text))

        full_text = "\n\n".join(paragraphs)

        return {
            "text": full_text,
            "paragraph_count": len(paragraphs),
            "has_text": len(full_text.strip()) > 0,
            "format": "docx",
            "is_scanned": False,
            "quality_score": 1.0  # DOCX is digital, high quality
        }

    except Exception as e:
        raise ValueError(f"Failed to parse DOCX: {str(e)}")


def extract_text(file_path: str) -> Dict[str, Any]:
    """
    Extract text from PDF or DOCX file
    Auto-detects format based on extension
    Automatically uses OCR for scanned PDFs

    Args:
        file_path: Path to file

    Returns:
        dict with extracted text and metadata
    """
    # Check if file exists
    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    file_path_lower = file_path.lower()

    if file_path_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_path)

    elif file_path_lower.endswith('.docx'):
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")
