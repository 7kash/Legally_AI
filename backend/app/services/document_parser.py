"""
Document parser service for extracting text from PDF and DOCX files
"""

from pathlib import Path
from typing import Dict, Any
import PyPDF2
from docx import Document


def extract_text_from_pdf(file_path: str) -> Dict[str, Any]:
    """
    Extract text from PDF file using PyPDF2

    Returns:
        dict with:
        - text: extracted text
        - page_count: number of pages
        - has_text: whether text was extracted
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            pages = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)

            full_text = "\n\n".join(pages)

            return {
                "text": full_text,
                "page_count": len(pdf_reader.pages),
                "has_text": len(full_text.strip()) > 0
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
            "has_text": len(full_text.strip()) > 0
        }

    except Exception as e:
        raise ValueError(f"Failed to parse DOCX: {str(e)}")


def extract_text(file_path: str) -> Dict[str, Any]:
    """
    Extract text from PDF or DOCX file
    Auto-detects format based on extension

    Args:
        file_path: Path to file

    Returns:
        dict with extracted text and metadata
    """
    file_path_lower = file_path.lower()

    if file_path_lower.endswith('.pdf'):
        result = extract_text_from_pdf(file_path)
        result['format'] = 'pdf'
        return result

    elif file_path_lower.endswith('.docx'):
        result = extract_text_from_docx(file_path)
        result['format'] = 'docx'
        return result

    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")
