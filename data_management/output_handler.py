# File: kazi/data_management/output_handler.py
# Content:
import os
from config import settings # Import settings from the config package

def save_text_to_output_dir(filename: str, content: str, subdirectory: str | None = None, base_file: str | None = None, app_type: str | None = None) -> str | None:
    """
    Saves text content to a file in the OUTPUT_DIR, organized by base file name and optionally by application type.
    Args:
        filename: The name of the file to save (e.g., "jd_analysis.md").
        content: The text content to save.
        subdirectory: Optional. A subdirectory within OUTPUT_DIR to save the file (e.g., "stage1").
        base_file: Optional. The base file name (without extension) of the input file (e.g., "wezesha_26_june_05").
        app_type: Optional. The application type (e.g., "consultancy", "consultancy-tailored", "job").
    Returns:
        The full path to the saved file, or None if an error occurs.
    """
    output_path = settings.OUTPUT_DIR
    if app_type:
        output_path = os.path.join(output_path, app_type)
    if base_file:
        output_path = os.path.join(output_path, base_file)
    if subdirectory:
        output_path = os.path.join(output_path, subdirectory)
    if not os.path.exists(output_path):
        try:
            os.makedirs(output_path)
            settings.log_info(f"Created output subdirectory: {output_path}")
        except Exception as e:
            settings.log_error(f"Could not create output subdirectory {output_path}: {e}")
            return None
    filepath = os.path.join(output_path, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        settings.log_info(f"Successfully saved output to {filepath}")
        return filepath
    except Exception as e:
        settings.log_error(f"Error: Could not save output file {filepath}: {e}")
        return None