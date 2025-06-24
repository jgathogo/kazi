# File: kazi/core/jd_analyzer.py
# Content:
from prompts.prompt_loader import load_prompt
from core.llm_interface import generate_text_from_prompt
from config import settings # Import settings from the config package

def analyze_job_description(jd_text: str) -> str | None:
    """
    Analyzes a job description using Prompt 1.
    Args:
        jd_text: The text content of the job description.
    Returns:
        The analysis result from the LLM as a Markdown string, or None if an error occurs.
    """
    if not jd_text:
        settings.log_error("JD text is empty. Cannot analyze.")
        return None

    # 1. Load Prompt 1 template
    prompt_template = load_prompt("jd_analysis_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load JD analysis prompt template.")
        return None

    # 2. Inject JD text into the prompt
    # The placeholder in jd_analysis_prompt.txt is "{{jd_text}}"
    final_prompt = prompt_template.replace("{{jd_text}}", jd_text)
    # settings.log_info(f"Final prompt for JD analysis (first 200 chars): {final_prompt[:200]}...") # For debugging

    # 3. Send to LLM and get response
    settings.log_info("Sending JD analysis prompt to LLM...")
    analysis_result = generate_text_from_prompt(final_prompt)

    if analysis_result:
        settings.log_info("Successfully received JD analysis from LLM.")
    else:
        settings.log_error("Failed to get JD analysis from LLM.")

    return analysis_result