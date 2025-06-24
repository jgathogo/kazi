# File: kazi/core/tor_analyzer.py
# New module for TOR analysis

from prompts.prompt_loader import load_prompt
from core.llm_interface import generate_text_from_prompt
from utils.text_utils import extract_json_from_response # To extract JSON from LLM response
from config import settings
import json

def analyze_terms_of_reference(tor_text: str) -> dict | None:
    """
    Analyzes a Terms of Reference (ToR) document using a specific prompt (Prompt 6).
    The LLM is instructed to return the analysis in a structured JSON format.

    Args:
        tor_text: The text content of the Terms of Reference.

    Returns:
        A dictionary parsed from the LLM's JSON response, or None if an error occurs
        or valid JSON cannot be extracted.
    """
    if not tor_text:
        settings.log_error("ToR text is empty. Cannot analyze.")
        return None

    # 1. Load Prompt 6 template (tor_analysis_prompt.txt)
    prompt_template = load_prompt("tor_analysis_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load ToR analysis prompt template (Prompt 6).")
        return None

    # 2. Inject ToR text into the prompt
    # The placeholder in tor_analysis_prompt.txt is "{{tor_text}}"
    final_prompt = prompt_template.replace("{{tor_text}}", tor_text)
    # settings.log_info(f"Final prompt for ToR analysis (first 200 chars): {final_prompt[:200]}...") # For debugging

    # 3. Send to LLM and get response
    settings.log_info("Sending ToR analysis prompt (Prompt 6) to LLM...")
    llm_response_text = generate_text_from_prompt(final_prompt)

    if not llm_response_text:
        settings.log_error("Failed to get response from LLM for ToR analysis.")
        return None

    # 4. Extract and parse the JSON block from the LLM's response
    tor_analysis_json_str = extract_json_from_response(llm_response_text)

    if tor_analysis_json_str:
        settings.log_info("Successfully extracted ToR analysis JSON from LLM response.")
        try:
            # Parse the JSON string into a Python dictionary
            tor_analysis_data = json.loads(tor_analysis_json_str)
            return tor_analysis_data
        except json.JSONDecodeError as e:
            settings.log_error(f"Failed to parse extracted ToR analysis JSON: {e}")
            settings.log_info(f"Problematic JSON string (first 500 chars): {tor_analysis_json_str[:500]}...")
            return None
    else:
        settings.log_error("Could not extract valid JSON for ToR analysis from LLM response.")
        settings.log_info(f"LLM Raw Response for Prompt 6 (first 500 chars for debugging):\n{llm_response_text[:500] if llm_response_text else 'None'}")
        return None

