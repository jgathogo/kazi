import json
from prompts.prompt_loader import load_prompt
from core.llm_interface import generate_text_from_prompt
from utils.text_utils import extract_json_from_response
from config import settings

def generate_jd_cv_mapping(jd_analysis_markdown: str, master_cv_data: dict) -> str | None:
    """
    Generates a mapping between JD requirements and Master CV content.
    Args:
        jd_analysis_markdown: The Markdown output from Prompt 1 (JD Analysis).
        master_cv_data: The full master CV data as a dictionary.
    Returns:
        A JSON string representing the mapping, or None if an error occurs.
    """
    settings.log_info("Initiating JD-CV Mapping generation (New Prompt).")

    prompt_template = load_prompt("jd_cv_mapping_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load JD-CV mapping prompt template.")
        return None

    try:
        master_cv_json_string = json.dumps(master_cv_data, indent=2)
    except TypeError as e:
        settings.log_error(f"Could not serialize master_cv_data to JSON for JD-CV mapping: {e}")
        return None

    # Prepare the full prompt for the LLM
    prompt_prefix = (
        "You have already performed a JD analysis (Prompt 1). Here is that analysis for your reference:\n\n"
        "--- BEGIN JD ANALYSIS (PROMPT 1 OUTPUT) ---\n"
        f"{jd_analysis_markdown}\n"
        "--- END JD ANALYSIS (PROMPT 1 OUTPUT) ---\n\n"
        "Here is the candidate's full Master CV data:\n\n"
        "--- BEGIN MASTER CV DATA ---\n"
        f"{master_cv_json_string}\n"
        "--- END MASTER CV DATA ---\n\n"
        "Now, please proceed with the following task (JD-CV Mapping Prompt):\n\n"
    )

    final_prompt_text = prompt_prefix + prompt_template

    settings.log_info("Sending JD-CV mapping prompt to LLM...")
    llm_response_text = generate_text_from_prompt(
        final_prompt_text,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS * 3 # Allow more tokens for detailed mapping
    )

    if not llm_response_text:
        settings.log_error("Failed to get response from LLM for JD-CV mapping.")
        return None

    # Assuming the LLM is instructed to output JSON
    jd_cv_mapping_json_str = extract_json_from_response(llm_response_text)

    if jd_cv_mapping_json_str:
        settings.log_info("Successfully extracted JD-CV mapping JSON from LLM response.")
        try:
            # Validate if it's parseable JSON
            json.loads(jd_cv_mapping_json_str)
            return jd_cv_mapping_json_str
        except json.JSONDecodeError as e:
            settings.log_error(f"Extracted string for JD-CV mapping is not valid JSON: {e}")
            settings.log_info(f"Problematic JSON string (first 500 chars): {jd_cv_mapping_json_str[:500]}...")
            return None
    else:
        settings.log_error("Could not extract valid JSON for JD-CV mapping from LLM response.")
        settings.log_info(f"LLM Raw Response for JD-CV Mapping (first 500 chars for debugging):\n{llm_response_text[:500] if llm_response_text else 'None'}")
        return None