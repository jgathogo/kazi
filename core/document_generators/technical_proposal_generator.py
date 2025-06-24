# File: kazi/core/document_generators/technical_proposal_generator.py

import json
import os # NEW: Import os for path operations
from prompts.prompt_loader import load_prompt
from core.llm_interface import generate_text_from_prompt
from utils.text_utils import extract_json_from_response
from config import settings
from data_management.input_handler import read_master_cv_json
import datetime


def generate_technical_approach_framework(tor_analysis_data: dict) -> dict | None:
    # ... (previous content of this function remains the same)
    settings.log_info("Initiating Technical Approach Framework generation (Prompt 7)...")

    prompt_template = load_prompt("technical_approach_framework_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load Technical Approach Framework prompt (Prompt 7) template.")
        return None

    try:
        # Convert the ToR analysis data to a JSON string for injection into the prompt
        tor_json_string = json.dumps(tor_analysis_data, indent=2)
    except TypeError as e:
        settings.log_error(f"Could not serialize ToR analysis data to JSON: {e}")
        return None

    # Replace the placeholder in the prompt template with the actual ToR analysis JSON
    final_prompt_text = prompt_template.replace("{{tor_analysis_json}}", tor_json_string)

    settings.log_info("Sending Technical Approach Framework prompt (Prompt 7) to LLM...")
    llm_response_text = generate_text_from_prompt(
        final_prompt_text,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS * 2 # Allow more tokens for structured output
    )

    if not llm_response_text:
        settings.log_error("Failed to get response from LLM for Technical Approach Framework.")
        return None

    # Extract the JSON array from the LLM's response
    framework_json_str = extract_json_from_response(llm_response_text) # This prompt outputs JSON

    if framework_json_str:
        settings.log_info("Successfully extracted Technical Approach Framework JSON from LLM response.")
        try:
            parsed_framework = json.loads(framework_json_str)
            if not isinstance(parsed_framework, list):
                settings.log_error("Extracted JSON for Technical Approach Framework is not a list.")
                return None
            return {"framework": parsed_framework} # Wrap in a dict for consistent return type if needed later
        except json.JSONDecodeError as e:
            settings.log_error(f"Extracted string for Technical Approach Framework is not valid JSON: {e}")
            settings.log_info(f"Problematic JSON string (first 500 chars): {framework_json_str[:500]}...")
            return None
    else:
        settings.log_error("Could not extract Technical Approach Framework JSON from LLM response.")
        settings.log_info(f"LLM Raw Response for Prompt 7 (first 500 chars for debugging):\n{llm_response_text[:500] if llm_response_text else 'None'}")
        return None


def generate_type_and_understanding_sections(tor_analysis_data: dict) -> str | None:
    # ... (previous content of this function remains the same)
    settings.log_info("Initiating Type and Understanding of Assignment sections generation (Prompt 8)...")

    prompt_template = load_prompt("understanding_assignment_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load Type and Understanding of Assignment prompt (Prompt 8) template.")
        return None

    try:
        # Convert the ToR analysis data to a JSON string for injection into the prompt
        tor_json_string = json.dumps(tor_analysis_data, indent=2)
    except TypeError as e:
        settings.log_error(f"Could not serialize ToR analysis data to JSON: {e}")
        return None

    # Replace the placeholder in the prompt template with the actual ToR analysis JSON
    final_prompt_text = prompt_template.replace("{{tor_analysis_json}}", tor_json_string)

    settings.log_info("Sending Type and Understanding of Assignment prompt (Prompt 8) to LLM...")
    llm_response_text = generate_text_from_prompt(
        final_prompt_text,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS * 2 # Allow more tokens for these sections
    )

    if llm_response_text:
        settings.log_info("Successfully received Type and Understanding of Assignment sections from LLM.")
        # Strip markdown fences if the LLM adds them
        stripped_content = llm_response_text
        if stripped_content.strip().startswith("```markdown"):
            stripped_content = stripped_content.strip()[len("```markdown"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ```markdown fences from LLM output for sections 4 and 5.")
        elif stripped_content.strip().startswith("```"): # Handle case where it's just ``` (no language)
            stripped_content = stripped_content.strip()[len("```"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ``` fences from LLM output for sections 4 and 5.")
        return stripped_content
    else:
        settings.log_error("Failed to get Type and Understanding of Assignment sections from LLM.")
        settings.log_info(f"LLM Raw Response for Prompt 8 (first 500 chars for debugging):\n{llm_response_text[:500] if llm_response_text else 'None'}")
        return None


def generate_detailed_technical_approach_sections(tor_analysis_data: dict) -> str | None:
    # ... (previous content of this function remains the same)
    settings.log_info("Initiating Detailed Technical Approach sections generation (Prompt 9)...")

    prompt_template = load_prompt("technical_approach_details_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load Detailed Technical Approach prompt (Prompt 9) template.")
        return None

    try:
        # Convert the ToR analysis data to a JSON string for injection into the prompt
        tor_json_string = json.dumps(tor_analysis_data, indent=2)
    except TypeError as e:
        settings.log_error(f"Could not serialize ToR analysis data to JSON: {e}")
        return None

    # Replace the placeholder in the prompt template with the actual ToR analysis JSON
    final_prompt_text = prompt_template.replace("{{tor_analysis_json}}", tor_json_string)

    settings.log_info("Sending Detailed Technical Approach prompt (Prompt 9) to LLM...")
    llm_response_text = generate_text_from_prompt(
        final_prompt_text,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS * 3 # Allow more tokens for these detailed sections
    )

    if llm_response_text:
        settings.log_info("Successfully received Detailed Technical Approach sections from LLM.")
        # Strip markdown fences if the LLM adds them
        stripped_content = llm_response_text
        if stripped_content.strip().startswith("```markdown"):
            stripped_content = stripped_content.strip()[len("```markdown"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ```markdown fences from LLM output for detailed technical approach.")
        elif stripped_content.strip().startswith("```"): # Handle case where it's just ``` (no language)
            stripped_content = stripped_content.strip()[len("```"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ``` fences from LLM output for detailed technical approach.")
        return stripped_content
    else:
        settings.log_error("Failed to get Detailed Technical Approach sections from LLM.")
        settings.log_info(f"LLM Raw Response for Prompt 9 (first 500 chars for debugging):\n{llm_response_text[:500] if llm_response_text else 'None'}")
        return None


def generate_work_plan_and_deliverables_sections(tor_analysis_data: dict) -> str | None:
    # ... (previous content of this function remains the same)
    settings.log_info("Initiating Work Plan and Deliverables sections generation (Prompt 10)...")

    prompt_template = load_prompt("work_plan_deliverables_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load Work Plan and Deliverables prompt (Prompt 10) template.")
        return None

    try:
        # Convert the ToR analysis data to a JSON string for injection into the prompt
        tor_json_string = json.dumps(tor_analysis_data, indent=2)
    except TypeError as e:
        settings.log_error(f"Could not serialize ToR analysis data to JSON: {e}")
        return None

    # Replace the placeholder in the prompt template with the actual ToR analysis JSON
    final_prompt_text = prompt_template.replace("{{tor_analysis_json}}", tor_json_string)

    settings.log_info("Sending Work Plan and Deliverables prompt (Prompt 10) to LLM...")
    llm_response_text = generate_text_from_prompt(
        final_prompt_text,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS * 3 # Allow more tokens for these detailed sections
    )

    if llm_response_text:
        settings.log_info("Successfully received Work Plan and Deliverables sections from LLM.")
        # Strip markdown fences if the LLM adds them
        stripped_content = llm_response_text
        if stripped_content.strip().startswith("```markdown"):
            stripped_content = stripped_content.strip()[len("```markdown"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ```markdown fences from LLM output for Work Plan and Deliverables.")
        elif stripped_content.strip().startswith("```"): # Handle case where it's just ``` (no language)
            stripped_content = stripped_content.strip()[len("```"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ``` fences from LLM output for Work Plan and Deliverables.")
        return stripped_content
    else:
        settings.log_error("Failed to get Work Plan and Deliverables sections from LLM.")
        settings.log_info(f"LLM Raw Response for Prompt 10 (first 500 chars for debugging):\n{llm_response_text[:500] if llm_response_text else 'None'}")
        return None


def generate_general_management_sections(tor_analysis_data: dict) -> str | None:
    # ... (previous content of this function remains the same)
    settings.log_info("Initiating General Management and Compliance sections generation (Prompt 11)...")

    prompt_template = load_prompt("general_management_sections_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load General Management and Compliance prompt (Prompt 11) template.")
        return None

    try:
        # Convert the ToR analysis data to a JSON string for injection into the prompt
        tor_json_string = json.dumps(tor_analysis_data, indent=2)
    except TypeError as e:
        settings.log_error(f"Could not serialize ToR analysis data to JSON: {e}")
        return None

    # Replace the placeholder in the prompt template with the actual ToR analysis JSON
    final_prompt_text = prompt_template.replace("{{tor_analysis_json}}", tor_json_string)

    settings.log_info("Sending General Management and Compliance prompt (Prompt 11) to LLM...")
    llm_response_text = generate_text_from_prompt(
        final_prompt_text,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS * 3 # Allow more tokens for these detailed sections
    )

    if llm_response_text:
        settings.log_info("Successfully received General Management and Compliance sections from LLM.")
        # Strip markdown fences if the LLM adds them
        stripped_content = llm_response_text
        if stripped_content.strip().startswith("```markdown"):
            stripped_content = stripped_content.strip()[len("```markdown"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ```markdown fences from LLM output for general management sections.")
        elif stripped_content.strip().startswith("```"): # Handle case where it's just ``` (no language)
            stripped_content = stripped_content.strip()[len("```"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ``` fences from LLM output for general management sections.")
        return stripped_content
    else:
        settings.log_error("Failed to get General Management and Compliance sections from LLM.")
        settings.log_info(f"LLM Raw Response for Prompt 11 (first 500 chars for debugging):\n{llm_response_text[:500] if llm_response_text else 'None'}")
        return None


def generate_team_and_experience_sections(tor_analysis_data: dict, master_cv_data: dict) -> str | None:
    # ... (previous content of this function remains the same)
    settings.log_info("Initiating Team Composition and Past Experience sections generation (Prompt 12)...")

    prompt_template = load_prompt("team_and_experience_sections_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load Team Composition and Past Experience prompt (Prompt 12) template.")
        return None

    try:
        # Convert both inputs to JSON strings for injection into the prompt
        tor_json_string = json.dumps(tor_analysis_data, indent=2)
        master_cv_json_string = json.dumps(master_cv_data, indent=2)
    except TypeError as e:
        settings.log_error(f"Could not serialize data to JSON for Prompt 12: {e}")
        return None

    # Replace the placeholders in the prompt template with the actual JSON inputs
    current_prompt_text = prompt_template.replace("{{tor_analysis_json}}", tor_json_string)
    final_prompt_text = current_prompt_text.replace("{{master_cv_data_json}}", master_cv_json_string)

    settings.log_info("Sending Team Composition and Past Experience prompt (Prompt 12) to LLM...")
    llm_response_text = generate_text_from_prompt(
        final_prompt_text,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS * 3 # Allow more tokens for these detailed sections
    )

    if llm_response_text:
        settings.log_info("Successfully received Team Composition and Past Experience sections from LLM.")
        # Strip markdown fences if the LLM adds them
        stripped_content = llm_response_text
        if stripped_content.strip().startswith("```markdown"):
            stripped_content = stripped_content.strip()[len("```markdown"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ```markdown fences from LLM output for team and experience sections.")
        elif stripped_content.strip().startswith("```"): # Handle case where it's just ``` (no language)
            stripped_content = stripped_content.strip()[len("```"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ``` fences from LLM output for team and experience sections.")
        return stripped_content
    else:
        settings.log_error("Failed to get Team Composition and Past Experience sections from LLM.")
        settings.log_info(f"LLM Raw Response for Prompt 12 (first 500 chars for debugging):\n{llm_response_text[:500] if llm_response_text else 'None'}")
        return None


def generate_executive_summary_section(
    tor_analysis_data: dict,
    technical_approach_framework: dict,
    type_and_understanding_md: str,
    detailed_technical_approach_md: str,
    work_plan_deliverables_md: str,
    team_and_experience_md: str,
    general_management_md: str
) -> str | None:
    # ... (previous content of this function remains the same)
    settings.log_info("Initiating Executive Summary generation (Prompt 13)...")

    prompt_template = load_prompt("executive_summary_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load Executive Summary prompt (Prompt 13) template.")
        return None

    try:
        # Convert inputs to JSON strings for injection into the prompt
        tor_json_string = json.dumps(tor_analysis_data, indent=2)
        framework_json_string = json.dumps(technical_approach_framework, indent=2)
    except TypeError as e:
        settings.log_error(f"Could not serialize JSON data for Prompt 13: {e}")
        return None

    # Replace placeholders in the prompt template
    current_prompt_text = prompt_template.replace("{{tor_analysis_json}}", tor_json_string)
    current_prompt_text = current_prompt_text.replace("{{technical_approach_framework_json}}", framework_json_string)
    current_prompt_text = current_prompt_text.replace("{{type_and_understanding_md}}", type_and_understanding_md)
    current_prompt_text = current_prompt_text.replace("{{detailed_technical_approach_md}}", detailed_technical_approach_md)
    current_prompt_text = current_prompt_text.replace("{{work_plan_deliverables_md}}", work_plan_deliverables_md)
    current_prompt_text = current_prompt_text.replace("{{team_and_experience_md}}", team_and_experience_md)
    final_prompt_text = current_prompt_text.replace("{{general_management_md}}", general_management_md)

    settings.log_info("Sending Executive Summary prompt (Prompt 13) to LLM...")
    llm_response_text = generate_text_from_prompt(
        final_prompt_text,
        max_output_tokens=settings.LLM_MAX_OUTPUT_TOKENS * 2 # Executive summary is shorter
    )

    if llm_response_text:
        settings.log_info("Successfully received Executive Summary from LLM.")
        stripped_content = llm_response_text
        if stripped_content.strip().startswith("```markdown"):
            stripped_content = stripped_content.strip()[len("```markdown"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ```markdown fences from LLM output for executive summary.")
        elif stripped_content.strip().startswith("```"):
            stripped_content = stripped_content.strip()[len("```"):].strip()
            if stripped_content.endswith("```"):
                stripped_content = stripped_content[:-len("```")].strip()
            settings.log_info("Stripped ``` fences from LLM output for executive summary.")
        return stripped_content
    else:
        settings.log_error("Failed to get Executive Summary from LLM.")
        settings.log_info(f"LLM Raw Response for Prompt 13 (first 500 chars for debugging):\n{llm_response_text[:500] if llm_response_text else 'None'}")
        return None


def assemble_technical_proposal_markdown(
    base_tor_filename: str,
    timestamp: str,
    llm_model_suffix: str,
    executive_summary_md: str,
    type_and_understanding_md: str,
    technical_approach_framework: dict, # JSON
    detailed_technical_approach_md: str,
    work_plan_deliverables_md: str,
    team_and_experience_md: str,
    general_management_md: str,
    master_cv_data: dict # To get candidate name for cover page
) -> str | None:
    """
    Assembles all generated Markdown content into a single, cohesive technical proposal document.
    Follows the structure outlined in technical_proposal_toc.md.
    """
    settings.log_info("Initiating Technical Proposal Assembly...")

    assembled_content = []

    # --- 1. Cover Page (Manual placeholders for now, LLM can generate later) ---
    # For a consolidated document, we'll just add a placeholder title.
    # Full cover page generation can be a separate LLM prompt if needed.
    proposal_title_from_tor = ""
    try:
        # Attempt to get the title from the tor_analysis_data if available
        # Note: tor_analysis_data is not passed directly here, so we'd need to re-read or pass it.
        # For simplicity in this assembly, let's use a generic title or pull from master_cv_data if needed
        if master_cv_data:
            consultant_name = master_cv_data.get("name", "Consultant Name")
        else:
            consultant_name = "Consultant Name"

        # Dynamically create the Proposal Title based on the original TOR filename
        # This assumes the TOR filename reflects the project title.
        # e.g., 'tor_childfund_pamoja_consultancy_29_may 25.pdf' -> 'Pamoja Consultancy'
        # Or ideally, retrieve from tor_analysis_data["title"] if that's available
        clean_base_name = base_tor_filename.replace("_", " ").replace("tor", "").strip()
        if clean_base_name.lower().startswith("childfund"): # Example specific cleaning
            clean_base_name = clean_base_name.replace("childfund", "ChildFund")
            if "consultancy" in clean_base_name:
                clean_base_name = clean_base_name.replace("consultancy", "Consultancy Proposal")
        elif clean_base_name.lower().startswith("consultant mid term evaluation"): # Example specific cleaning for Oxfam
             clean_base_name = "Mid-Term Evaluation Technical Proposal"


        proposal_title = f"{clean_base_name.title()} - Technical Proposal"

        assembled_content.append(f"# {proposal_title}\n\n")
        assembled_content.append(f"**ToR Reference:** {base_tor_filename}\n")
        assembled_content.append(f"**Date of Submission:** {datetime.date.today().strftime('%d %B %Y')}\n")
        assembled_content.append(f"**Lead Consultant/Organisation:** {consultant_name}\n")
        assembled_content.append("\n<div class='page'></div>\n") # Page break

    except Exception as e:
        settings.log_error(f"Error generating Cover Page elements during assembly: {e}")
        assembled_content.append("# Technical Proposal\n\n") # Fallback

    # --- 2. Table of Contents (Placeholder for now, could be auto-generated in PDF conversion) ---
    assembled_content.append("## 2. Table of Contents\n\n")
    assembled_content.append("*This section will contain a detailed Table of Contents upon final document generation.*\n\n")
    assembled_content.append("\n<div class='page'></div>\n") # Page break

    # --- 3. Executive Summary ---
    if executive_summary_md:
        assembled_content.append(executive_summary_md)
        assembled_content.append("\n\n<div class='page'></div>\n") # Page break
    else:
        assembled_content.append("## 3. Executive Summary\n*Content not available.*\n\n<div class='page'></div>\n")


    # --- 4. Type of Assignment ---
    if type_and_understanding_md:
        # Extract only Section 4 from type_and_understanding_md for logical flow
        # This requires parsing the MD, which is tricky. For now, assume entire MD
        # For a true modular assembly, Prompt 8 should ideally output 2 separate MD strings or a JSON
        # containing both sections. Given current Prompt 8, we'll include it fully.
        # This will contain both Section 4 and Section 5 headings.
        assembled_content.append(type_and_understanding_md)
        assembled_content.append("\n\n<div class='page'></div>\n") # Page break
    else:
        assembled_content.append("## 4. Type of Assignment\n*Content not available.*\n\n")
        assembled_content.append("## 5. Understanding of the Assignment\n*Content not available.*\n\n<div class='page'></div>\n")


    # --- 6. Technical Approach and Methodology ---
    assembled_content.append("## 6. Technical Approach and Methodology\n\n")

    # 6.1. Proposed Technical Approach Framework (from JSON)
    if technical_approach_framework and technical_approach_framework.get("framework"):
        assembled_content.append("### 6.1. Proposed Technical Approach Framework\n\n")
        assembled_content.append("| Criteria | Question | Proposed Method(s) | Justification |\n")
        assembled_content.append("|---|---|---|---|\n")
        for row in technical_approach_framework["framework"]:
            criteria = row.get("criteria", "N/A").replace("|", "\\|")
            question = row.get("question", "N/A").replace("|", "\\|")
            methods = ", ".join(row.get("proposed_method_s", [])).replace("|", "\\|")
            justification = row.get("justification", "N/A").replace("|", "\\|")
            assembled_content.append(f"| {criteria} | {question} | {methods} | {justification} |\n")
        assembled_content.append("\n") # Add a newline after table
    else:
        assembled_content.append("### 6.1. Proposed Technical Approach Framework\n*Content not available or invalid.*\n\n")

    # 6.2-6.10. Detailed Technical Approach (from MD)
    if detailed_technical_approach_md:
        assembled_content.append(detailed_technical_approach_md)
    else:
        assembled_content.append("### 6.2. Overall Strategy and Guiding Principles\n*Content not available.*\n\n")
        assembled_content.append("### 6.3. Methodological Framework\n*Content not available.*\n\n")
        assembled_content.append("### 6.4. Data Collection and Analysis Plans\n*Content not available.*\n\n")
        assembled_content.append("### 6.5. Sampling Approach\n*Content not available.*\n\n")
        assembled_content.append("### 6.6. Evaluation Criteria and Indicators\n*Content not available.*\n\n")
        assembled_content.append("### 6.7. Gender, Equity and Rights-based Integration\n*Content not available.*\n\n")
        assembled_content.append("### 6.8. Risk Management Strategy (Technical aspects)\n*Content not available.*\n\n")
        assembled_content.append("### 6.9. Ethical Considerations and Data Protection\n*Content not available.*\n\n")
        assembled_content.append("### 6.10. Limitations and Mitigation\n*Content not available.*\n\n")

    assembled_content.append("\n<div class='page'></div>\n") # Page break


    # --- 7. Work Plan and Deliverables ---
    if work_plan_deliverables_md:
        assembled_content.append(work_plan_deliverables_md)
        assembled_content.append("\n\n<div class='page'></div>\n") # Page break
    else:
        assembled_content.append("## 7. Work Plan and Deliverables\n*Content not available.*\n\n<div class='page'></div>\n")


    # --- 8. Team Composition and Organisational Capacity & 9. Past Experience and Relevant Projects ---
    if team_and_experience_md:
        assembled_content.append(team_and_experience_md)
        assembled_content.append("\n\n<div class='page'></div>\n") # Page break
    else:
        assembled_content.append("## 8. Team Composition and Organisational Capacity\n*Content not available.*\n\n")
        assembled_content.append("## 9. Past Experience and Relevant Projects\n*Content not available.*\n\n<div class='page'></div>\n")


    # --- 10. Quality Assurance and Risk Management, 11. Management and Coordination,
    #      12. Ethical Standards and Safeguarding, 13. Compliance with Terms of Reference ---
    if general_management_md:
        assembled_content.append(general_management_md)
        assembled_content.append("\n\n<div class='page'></div>\n") # Page break
    else:
        assembled_content.append("## 10. Quality Assurance and Risk Management\n*Content not available.*\n\n")
        assembled_content.append("## 11. Management and Coordination\n*Content not available.*\n\n")
        assembled_content.append("## 12. Ethical Standards and Safeguarding\n*Content not available.*\n\n")
        assembled_content.append("## 13. Compliance with Terms of Reference\n*Content not available.*\n\n<div class='page'></div>\n")

    # --- 14. Annexes (Placeholder, actual annexes are separate files) ---
    assembled_content.append("## 14. Annexes\n\n")
    assembled_content.append("This section will contain supporting documents, such as:\n")
    assembled_content.append("- Detailed CVs of Key Personnel\n")
    assembled_content.append("- Gantt Chart\n")
    assembled_content.append("- Organogram\n")
    assembled_content.append("- Letters of Reference or Support (if requested)\n")
    assembled_content.append("- Company Registration, Legal Status\n")
    assembled_content.append("- Safeguarding and Ethics Policies\n")
    assembled_content.append("- Sample Outputs from Past Work (if allowed)\n")
    assembled_content.append("- Financial Capacity Statements (if requested)\n")


    final_assembled_markdown = "\n".join(assembled_content)
    settings.log_info("Technical Proposal Assembly completed.")
    return final_assembled_markdown

