# File: kazi/core/document_generators/cv_generator.py
# Create this new file
import json
import re 
from prompts.prompt_loader import load_prompt
from core.llm_interface import generate_text_from_prompt
from utils.text_utils import extract_json_from_response
from utils.static_content_builder import ( 
    build_personal_md,
    build_education_md,
    build_certifications_md,
    build_publications_md,
    build_languages_md
)
from config import settings

def generate_tailored_experience_json(jd_analysis_markdown: str, master_cv_data: dict) -> str | None:
    # ... (previous content of this function remains the same)
    if not master_cv_data:
        settings.log_error("Master CV data is empty. Cannot generate tailored experience.")
        return None
    if not jd_analysis_markdown:
        settings.log_info("Warning: JD analysis is missing, tailoring might be suboptimal.")

    prompt_template = load_prompt("cv_tailoring_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load CV tailoring prompt (Prompt 2) template.")
        return None
    try:
        cv_json_string = json.dumps(master_cv_data, indent=2)
    except TypeError as e:
        settings.log_error(f"Could not serialize master_cv_data to JSON: {e}")
        return None
    
    prompt_prefix = (
        "You have already performed a JD analysis (Prompt 1). Here is that analysis for your reference:\n\n"
        "--- BEGIN JD ANALYSIS (PROMPT 1 OUTPUT) ---\n"
        f"{jd_analysis_markdown}\n"
        "--- END JD ANALYSIS (PROMPT 1 OUTPUT) ---\n\n"
        "Now, please proceed with the following task (Prompt 2), using the JD analysis above and the provided CV data:\n\n"
    )
    final_prompt_text = prompt_prefix + prompt_template.replace("{{cv_json_data}}", cv_json_string)
    settings.log_info("Sending CV tailoring prompt (Prompt 2) to LLM...")
    llm_response_text = generate_text_from_prompt(final_prompt_text)

    if not llm_response_text:
        settings.log_error("Failed to get response from LLM for CV tailoring.")
        return None
    tailored_experience_json_str = extract_json_from_response(llm_response_text)

    if tailored_experience_json_str:
        settings.log_info("Successfully extracted tailored experience JSON from LLM response.")
        try:
            parsed_json = json.loads(tailored_experience_json_str)
            if not isinstance(parsed_json, list):
                settings.log_error("Extracted JSON for tailored experience is not a list.")
        except json.JSONDecodeError:
            settings.log_error("Extracted string for tailored experience is not valid JSON.")
            return None
    else:
        settings.log_error("Could not extract tailored experience JSON from LLM response.")
        settings.log_info(f"LLM Raw Response for Prompt 2 (first 500 chars for debugging):\n{llm_response_text[:500]}")
    return tailored_experience_json_str


def assemble_final_cv_markdown(
    jd_analysis_markdown: str, 
    tailored_experience_json_str: str, 
    strategic_narrative_markdown: str, 
    master_cv_data: dict
) -> str | None:
    settings.log_info("Initiating CV assembly (Prompt 4)...")

    personal_md = build_personal_md(master_cv_data)
    education_md = build_education_md(master_cv_data.get("education"))
    certifications_md = build_certifications_md(master_cv_data.get("certifications"))
    publications_md = build_publications_md(master_cv_data.get("publications"))
    languages_md = build_languages_md(master_cv_data.get("languages"))

    summary_match = re.search(r"### Professional Summary\s*([\s\S]*?)(?=\n###|$)", strategic_narrative_markdown, re.IGNORECASE | re.DOTALL)
    professional_summary_content = ""
    if summary_match:
        professional_summary_content = summary_match.group(1).strip()
        settings.log_info("Successfully extracted Professional Summary for CV assembly.")
    else:
        settings.log_error("Could not extract Professional Summary from Prompt 3 output. CV will lack this section.")
    
    professional_summary_md_section = f"## Professional Summary\n{professional_summary_content}"

    prompt_template = load_prompt("cv_assembly_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load CV assembly prompt (Prompt 4) template.")
        return None
    
    prompt_prefix = (
        "You have already performed a JD analysis (Prompt 1) and generated tailored work experiences (Prompt 2 output). "
        "Here they are for your reference to help you complete the 'Key Skills & Tools' section and format the 'Experience' section:\n\n"
        "--- BEGIN JD ANALYSIS (PROMPT 1 OUTPUT) ---\n"
        f"{jd_analysis_markdown}\n"
        "--- END JD ANALYSIS (PROMPT 1 OUTPUT) ---\n\n"
        "Now, please assemble the CV using the provided placeholders and the context above:\n\n"
    )

    current_prompt_text = prompt_template
    current_prompt_text = current_prompt_text.replace("{{personal_md_section}}", personal_md if personal_md else "")
    current_prompt_text = current_prompt_text.replace("{{professional_summary_section}}", professional_summary_md_section if professional_summary_md_section else "## Professional Summary\n")
    current_prompt_text = current_prompt_text.replace("{{tailored_experience_json}}", tailored_experience_json_str if tailored_experience_json_str else "[]") 
    current_prompt_text = current_prompt_text.replace("{{education_md_section}}", education_md if education_md else "## Education\n")
    current_prompt_text = current_prompt_text.replace("{{certifications_md_section}}", certifications_md if certifications_md else "## Certifications\n")
    current_prompt_text = current_prompt_text.replace("{{publications_md_section}}", publications_md if publications_md else "## Publications\n")
    current_prompt_text = current_prompt_text.replace("{{languages_md_section}}", languages_md if languages_md else "## Languages\n")
    
    final_prompt_text = prompt_prefix + current_prompt_text
    
    settings.log_info("Sending CV assembly prompt (Prompt 4) to LLM...")
    llm_generated_cv_markdown = generate_text_from_prompt(final_prompt_text, max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS * 2) 

    if llm_generated_cv_markdown:
        settings.log_info("Successfully received final CV Markdown from LLM.")
        
        # ---- NEW: Strip ```markdown fences ----
        stripped_cv_markdown = llm_generated_cv_markdown
        if stripped_cv_markdown.strip().startswith("```markdown"):
            stripped_cv_markdown = stripped_cv_markdown.strip()[len("```markdown"):].strip()
            # Remove the trailing ``` if it exists
            if stripped_cv_markdown.endswith("```"):
                stripped_cv_markdown = stripped_cv_markdown[:-len("```")].strip()
            settings.log_info("Stripped ```markdown fences from LLM CV output.")
        elif stripped_cv_markdown.strip().startswith("```"): # Handle case where it's just ``` (no language)
            stripped_cv_markdown = stripped_cv_markdown.strip()[len("```"):].strip()
            if stripped_cv_markdown.endswith("```"):
                stripped_cv_markdown = stripped_cv_markdown[:-len("```")].strip()
            settings.log_info("Stripped ``` fences from LLM CV output.")
        
        return stripped_cv_markdown # Return the stripped version
        # ---- END NEW ----
    else:
        settings.log_error("Failed to get final CV Markdown from LLM for Prompt 4.")
        settings.log_info(f"LLM Raw Response for Prompt 4 (first 500 chars for debugging):\n{llm_generated_cv_markdown[:500] if llm_generated_cv_markdown else 'None'}")
        return None # Explicitly return None on failure