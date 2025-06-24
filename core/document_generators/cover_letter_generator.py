# File: kazi/core/document_generators/cover_letter_generator.py
# Create this new file
import re
from prompts.prompt_loader import load_prompt
from core.llm_interface import generate_text_from_prompt
from config import settings
import datetime
import json

def extract_info_from_jd_analysis(jd_analysis_markdown: str) -> dict:
    """
    Extracts Job Title and Organization from the JD Analysis (Prompt 1 output).
    Args:
        jd_analysis_markdown: The Markdown output from Prompt 1.
    Returns:
        A dictionary with "job_title" and "organisation_name".
    """
    info = {"job_title": "The Position", "organisation_name": "The Organisation"} # Defaults

    # Extract Job Title
    # Looks for "* **Job Title:** Actual Job Title"
    title_match = re.search(r"\* \*\*Job Title:\*\*\s*(.*)", jd_analysis_markdown)
    if title_match:
        info["job_title"] = title_match.group(1).strip()

    # Extract Organization
    # Looks for "* **Organization:** Actual Organization Name"
    org_match = re.search(r"\* \*\*Organization:\*\*\s*(.*)", jd_analysis_markdown)
    if org_match:
        info["organisation_name"] = org_match.group(1).strip()
    
    settings.log_info(f"Extracted for Cover Letter: Title='{info['job_title']}', Organisation='{info['organisation_name']}'")
    return info


def generate_cover_letter_markdown(
    jd_analysis_markdown: str,
    tailored_experience_json_str: str, # Keep for now if any part of Prompt 5 still refers to it, though mapping is primary
    strategic_narrative_markdown: str,
    master_cv_data: dict, # For candidate's name and contact details
    jd_cv_mapping_json_str: str # NEW: Add this parameter
) -> str | None:
    """
    Generates a tailored cover letter using Prompt 5, now primarily based on JD-CV mapping.
    Args:
        jd_analysis_markdown: Output from Prompt 1.
        tailored_experience_json_str: JSON string output from Prompt 2. (Less primary now)
        strategic_narrative_markdown: Markdown output from Prompt 3.
        master_cv_data: Full master CV data for candidate's name and contact details.
        jd_cv_mapping_json_str: JSON string of the JD-CV mapping generated in the new step.
    Returns:
        The cover letter as a Markdown string, or None if an error occurs.
    """
    settings.log_info("Initiating Cover Letter generation (Prompt 5) with JD-CV mapping...")

    # 1. Extract Job Title and Organisation Name from JD Analysis
    job_details = extract_info_from_jd_analysis(jd_analysis_markdown)
    job_title = job_details["job_title"]
    organisation_name = job_details["organisation_name"]
    
    # 2. Extract Candidate's Name and Contact Details from master_cv_data
    candidate_name = master_cv_data.get("name", "The Candidate")
    candidate_phone = master_cv_data.get("phone", "")
    candidate_email = master_cv_data.get("email", "")
    candidate_linkedin = master_cv_data.get("linkedin", "")

    # Format contact details for Markdown
    contact_parts = []
    if candidate_phone:
        tel_phone = ''.join(filter(lambda char: char.isdigit() or char == '+', candidate_phone))
        if candidate_phone.startswith('+') and not tel_phone.startswith('+'):
            tel_phone = '+' + tel_phone
        contact_parts.append(f"[{candidate_phone}](tel:{tel_phone})")
    if candidate_email:
        contact_parts.append(f"[{candidate_email}](mailto:{candidate_email})")
    if candidate_linkedin:
        linkedin_display = candidate_linkedin.replace('https://','').replace('http://','')
        contact_parts.append(f"LinkedIn: [{linkedin_display}]({candidate_linkedin})")
    
    formatted_contact_details = " | ".join(contact_parts)
    
    # 3. Get current date
    current_date = datetime.date.today().strftime("%d %B %Y") # e.g., "21 May 2025"

    # 4. Load Prompt 5 template
    prompt_template = load_prompt("cover_letter_generation_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load cover letter generation prompt (Prompt 5) template.")
        return None

    # 5. Prepare the full prompt for the LLM (Prompt 5)
    # The prompt should now emphasize using jd_cv_mapping_json_str primarily
    prompt_prefix = (
        "You have already performed a JD analysis (Prompt 1), generated tailored work experiences (Prompt 2), "
        "and synthesized a strategic narrative (Prompt 3). MOST IMPORTANTLY, you have generated a detailed "
        "JD-CV mapping (New Mapping Prompt). Here is a summary of that information for your reference:\n\n"
        "--- BEGIN JD ANALYSIS (PROMPT 1 OUTPUT) ---\n"
        f"{jd_analysis_markdown}\n"
        "--- END JD ANALYSIS (PROMPT 1 OUTPUT) ---\n\n"
        "--- BEGIN TAILORED EXPERIENCE JSON (PROMPT 2 OUTPUT) ---\n" # Keeping for completeness if prompt still references
        f"{tailored_experience_json_str}\n"
        "--- END TAILORED EXPERIENCE JSON (PROMPT 2 OUTPUT) ---\n\n"
        "--- BEGIN STRATEGIC NARRATIVE & SUMMARY (PROMPT 3 OUTPUT) ---\n"
        f"{strategic_narrative_markdown}\n"
        "--- END STRATEGIC NARRATIVE & SUMMARY (PROMPT 3 OUTPUT) ---\n\n"
        "--- BEGIN JD-CV MAPPING (NEW MAPPING PROMPT OUTPUT) ---\n" # NEW: Add the mapping here
        f"{jd_cv_mapping_json_str}\n"
        "--- END JD-CV MAPPING (NEW MAPPING PROMPT OUTPUT) ---\n\n"
        # Pass additional dynamic data
        f"The candidate's name is: {candidate_name}\n"
        f"The candidate's contact details are: {formatted_contact_details}\n"
        f"Today's date is: {current_date}\n\n"
        "Now, please craft the cover letter based on the following instructions (Prompt 5). "
        "You MUST primarily use the 'JD-CV MAPPING' content to construct the body paragraphs, "
        "ensuring every claim in the cover letter is directly supported by the mapped evidence from the CV:\n\n"
    )

    # Replace placeholders in Prompt 5 template
    current_prompt_text = prompt_template
    current_prompt_text = current_prompt_text.replace("{{job_title}}", job_title)
    current_prompt_text = current_prompt_text.replace("{{organisation_name}}", organisation_name)
    
    # NEW: Replace placeholders for dynamic header
    current_prompt_text = current_prompt_text.replace("{{candidate_name}}", candidate_name)
    current_prompt_text = current_prompt_text.replace("{{formatted_contact_details}}", formatted_contact_details)
    current_prompt_text = current_prompt_text.replace("{{current_date}}", current_date)
    # NEW: Add mapping content placeholder (even though it's already in prompt_prefix, useful for clarity in prompt itself)
    current_prompt_text = current_prompt_text.replace("{{jd_cv_mapping_content}}", jd_cv_mapping_json_str)

    final_prompt_text = prompt_prefix + current_prompt_text
    
    # 6. Send to LLM
    settings.log_info("Sending Cover Letter generation prompt (Prompt 5) to LLM...")
    cover_letter_md = generate_text_from_prompt(final_prompt_text, max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS) 

    if cover_letter_md:
        settings.log_info("Successfully received Cover Letter Markdown from LLM.")
        
        stripped_cover_letter_markdown = cover_letter_md
        if stripped_cover_letter_markdown.strip().startswith("```markdown"):
            stripped_cover_letter_markdown = stripped_cover_letter_markdown.strip()[len("```markdown"):].strip()
            # Remove the trailing ``` if it exists
            if stripped_cover_letter_markdown.endswith("```"):
                stripped_cover_letter_markdown = stripped_cover_letter_markdown[:-len("```")].strip()
            settings.log_info("Stripped ```markdown fences from LLM Cover Letter output.")
        elif stripped_cover_letter_markdown.strip().startswith("```"): # Handle case where it's just ``` (no language)
            stripped_cover_letter_markdown = stripped_cover_letter_markdown.strip()[len("```"):].strip()
            if stripped_cover_letter_markdown.endswith("```"):
                stripped_cover_letter_markdown = stripped_cover_letter_markdown[:-len("```")].strip()
            settings.log_info("Stripped ``` fences from LLM Cover Letter output.")
        
        return stripped_cover_letter_markdown # Return the stripped version
        
    else:
        settings.log_error("Failed to get Cover Letter Markdown from LLM for Prompt 5.")
        settings.log_info(f"LLM Raw Response for Prompt 5 (first 500 chars for debugging):\n{cover_letter_md[:500] if cover_letter_md else 'None'}")

    return cover_letter_md