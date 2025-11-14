"""
Document text extraction service for PDF and DOCX files.

This module provides utilities to extract text content from uploaded contract documents.
"""

import os
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text as a string

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If PDF parsing fails
    """
    try:
        # Try newer pypdf first, fall back to PyPDF2
        try:
            from pypdf import PdfReader
        except ImportError:
            from PyPDF2 import PdfReader
    except ImportError:
        logger.error("pypdf/PyPDF2 not installed. Install with: pip install pypdf2")
        raise ImportError("pypdf/PyPDF2 library is required for PDF extraction")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    text_content = []

    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)

            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num + 1}: {e}")
                    continue

        extracted_text = "\n\n".join(text_content)
        logger.info(f"Extracted {len(extracted_text)} characters from PDF: {file_path}")
        return extracted_text

    except Exception as e:
        logger.error(f"Failed to parse PDF {file_path}: {e}")
        raise Exception(f"PDF parsing failed: {str(e)}")


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.

    Args:
        file_path: Path to the DOCX file

    Returns:
        Extracted text as a string

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If DOCX parsing fails
    """
    try:
        from docx import Document
    except ImportError:
        logger.error("python-docx not installed. Install with: pip install python-docx")
        raise ImportError("python-docx library is required for DOCX extraction")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"DOCX file not found: {file_path}")

    try:
        doc = Document(file_path)

        # Extract text from paragraphs
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]

        # Extract text from tables
        table_text = []
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells]
                if any(row_text):  # Only add non-empty rows
                    table_text.append(" | ".join(row_text))

        # Combine all text
        all_text = paragraphs + table_text
        extracted_text = "\n\n".join(all_text)

        logger.info(f"Extracted {len(extracted_text)} characters from DOCX: {file_path}")
        return extracted_text

    except Exception as e:
        logger.error(f"Failed to parse DOCX {file_path}: {e}")
        raise Exception(f"DOCX parsing failed: {str(e)}")


def extract_text_from_document(file_path: str) -> Tuple[str, int]:
    """
    Extract text from a document file (PDF or DOCX).

    Automatically detects file type based on extension and uses appropriate parser.

    Args:
        file_path: Path to the document file

    Returns:
        Tuple of (extracted_text, character_count)

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file type is not supported
        Exception: If text extraction fails
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document file not found: {file_path}")

    # Get file extension
    file_ext = Path(file_path).suffix.lower()

    # Extract text based on file type
    if file_ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_ext in ['.docx', '.doc']:
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}. Supported types: .pdf, .docx, .doc")

    char_count = len(text)

    if char_count == 0:
        logger.warning(f"No text extracted from {file_path}. File may be empty or image-based.")

    return text, char_count


def get_document_path(contract_id: str, user_id: str, file_extension: str, uploads_dir: str = "/app/uploads") -> str:
    """
    Construct the full path to an uploaded document.

    Args:
        contract_id: UUID of the contract
        user_id: UUID of the user
        file_extension: File extension (e.g., '.pdf', '.docx')
        uploads_dir: Base uploads directory (default: /app/uploads)

    Returns:
        Full path to the document file
    """
    return os.path.join(uploads_dir, str(user_id), f"{contract_id}{file_extension}")


def validate_document_exists(file_path: str) -> bool:
    """
    Check if a document file exists and is readable.

    Args:
        file_path: Path to the document file

    Returns:
        True if file exists and is readable, False otherwise
    """
    if not os.path.exists(file_path):
        logger.error(f"Document file not found: {file_path}")
        return False

    if not os.path.isfile(file_path):
        logger.error(f"Path is not a file: {file_path}")
        return False

    if not os.access(file_path, os.R_OK):
        logger.error(f"File is not readable: {file_path}")
        return False

    return True
