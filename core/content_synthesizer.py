# File: kazi/core/content_synthesizer.py
# Create this new file
from prompts.prompt_loader import load_prompt
from core.llm_interface import generate_text_from_prompt
from config import settings

def generate_strategic_narrative(jd_analysis_markdown: str, tailored_experience_json_str: str) -> str | None:
    """
    Generates the strategic fit narrative, key selling points, and professional summary (Prompt 3).
    Args:
        jd_analysis_markdown: The Markdown string output from Prompt 1 (JD Analysis).
        tailored_experience_json_str: The JSON string of tailored assignments from Prompt 2.
    Returns:
        A Markdown string containing the generated content, or None if an error occurs.
    """
    if not jd_analysis_markdown:
        settings.log_error("JD analysis is empty. Cannot generate strategic narrative effectively.")
        # Consider if you want to proceed or return None
        settings.log_info("Warning: JD analysis is missing, strategic narrative might be suboptimal.")
        # return None
    if not tailored_experience_json_str:
        settings.log_error("Tailored experience JSON is empty. Cannot generate strategic narrative.")
        return None

    # 1. Load Prompt 3 template
    prompt_template = load_prompt("summary_generation_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load summary generation prompt (Prompt 3) template.")
        return None

    # 2. Prepare the full prompt for the LLM
    # Similar to Prompt 2, we prepend the JD analysis for context, as Prompt 3
    # also refers to it as if it's in chat history.
    prompt_prefix = (
        "You have already performed a JD analysis (Prompt 1). Here is that analysis for your reference:\n\n"
        "--- BEGIN JD ANALYSIS (PROMPT 1 OUTPUT) ---\n"
        f"{jd_analysis_markdown}\n"
        "--- END JD ANALYSIS (PROMPT 1 OUTPUT) ---\n\n"
        "You have also generated a tailored list of work experiences (Prompt 2 output). "
        "Now, please proceed with the following task (Prompt 3), using the JD analysis above and the provided tailored work experience JSON:\n\n"
    )

    # Inject the tailored_experience_json_str into the placeholder
    # The placeholder in summary_generation_prompt.txt is {{tailored_work_experience_json}}
    prompt_with_cv_data = prompt_template.replace("{{tailored_work_experience_json}}", tailored_experience_json_str)
    
    final_prompt_text = prompt_prefix + prompt_with_cv_data
    # settings.log_info(f"Final prompt for strategic narrative (first 300 chars): {final_prompt_text[:300]}...") # For debugging

    # 3. Send to LLM
    settings.log_info("Sending strategic narrative prompt (Prompt 3) to LLM...")
    narrative_markdown = generate_text_from_prompt(final_prompt_text)

    if narrative_markdown:
        settings.log_info("Successfully received strategic narrative from LLM.")
    else:
        settings.log_error("Failed to get strategic narrative from LLM.")
        settings.log_info(f"LLM Raw Response for Prompt 3 (first 500 chars for debugging):\n{narrative_markdown[:500] if narrative_markdown else 'None'}")


    return narrative_markdown