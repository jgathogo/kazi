# File: kazi/data_management/input_handler.py
# Content:
import os
import json
from pdfminer.high_level import extract_text as pdfminer_extract_text
from config import settings

def read_pdf_text(filepath: str) -> str | None:
    """
    Reads text content from a PDF file.
    Args:
        filepath: The absolute or relative path to the PDF file.
    Returns:
        The extracted text content, or None if an error occurs.
    """
    settings.log_info(f"Attempting to read PDF from: {filepath}")
    try:
        text = pdfminer_extract_text(filepath)
        settings.log_info(f"Successfully extracted text from PDF: {filepath}")
        return text
    except FileNotFoundError:
        settings.log_error(f"PDF file not found at: {filepath}")
        return None
    except Exception as e:
        settings.log_error(f"An unexpected error occurred while reading PDF {filepath}: {e}")
        return None

def read_pdf_text_from_jd_storage(jd_filename_arg: str) -> str | None:
    """
    Reads text content from a JD PDF file located in the JD_STORAGE_DIR.
    This function now uses the more generic 'read_pdf_text'.
    """
    actual_filename = os.path.basename(jd_filename_arg)
    filepath = os.path.join(settings.JD_STORAGE_DIR, actual_filename)
    return read_pdf_text(filepath)

def read_pdf_text_from_tor_storage(tor_filename_arg: str) -> str | None:
    """
    Reads text content from a ToR PDF file located in the TOR_STORAGE_DIR.
    This is a new function for consultancy ToRs.
    """
    actual_filename = os.path.basename(tor_filename_arg)
    filepath = os.path.join(settings.TOR_STORAGE_DIR, actual_filename)
    return read_pdf_text(filepath)

def read_master_cv_json() -> dict | None:
    """
    Reads the master CV JSON file from the CV_DATA_DIR.
    Returns:
        A dictionary parsed from the master CV JSON, or None if an error occurs.
    """
    filepath = os.path.join(settings.CV_DATA_DIR, settings.MASTER_CV_FILENAME)
    settings.log_info(f"Attempting to read master CV JSON from: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        settings.log_info(f"Successfully read and parsed master CV JSON from {filepath}")
        return data
    except FileNotFoundError:
        settings.log_error(f"Master CV JSON file not found at: {filepath}. Please ensure '{settings.MASTER_CV_FILENAME}' exists in '{settings.CV_DATA_DIR}'.")
        return None
    except json.JSONDecodeError:
        settings.log_error(f"Could not decode JSON from {filepath}. Check master CV file format.")
        return None
    except Exception as e:
        settings.log_error(f"An unexpected error occurred while reading master CV JSON {filepath}: {e}")
        return None

