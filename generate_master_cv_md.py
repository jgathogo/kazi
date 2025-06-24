# File: kazi-main/generate_master_cv_md.py

import os
import json
from datetime import datetime # For current year for "Present" date ranges
import re # NEW: Import re for regex operations

# Import necessary functions from utils.static_content_builder
# Assuming this script is run from kazi-main/
# Adjust imports if you place this script in a different subdirectory
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'data_management'))

from static_content_builder import (
    build_personal_md,
    build_education_md,
    build_certifications_md,
    build_publications_md,
    build_languages_md,
    format_date_for_cv # Re-using this utility for date formatting
)
from input_handler import read_master_cv_json
from output_handler import save_text_to_output_dir
from settings import log_info, log_error, CV_DATA_DIR, MASTER_CV_FILENAME # Import settings for paths and logging

def build_master_experience_md(assignments_list: list | None) -> str:
    """
    Builds the 'Experience' section for the master CV from all assignments.
    Excludes 'id' fields and formats as H3 title, italicized org/loc/date, and bulleted tasks.
    Ensures correct bullet point formatting by stripping existing list markers.
    """
    if not assignments_list:
        return "## Experience\n*No experience data provided.*"

    md_parts = ["## Experience", ""]

    # Sort assignments by start_date (most recent first)
    def get_assignment_sort_key(assignment_item):
        start_date_str = assignment_item.get("start_date")
        if start_date_str:
            try:
                return datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                # Fallback for other date formats if needed, or just use a default early date
                return datetime.min
        return datetime.min # Default for items with no start date

    sorted_assignments = sorted(assignments_list, key=get_assignment_sort_key, reverse=True)

    for assignment in sorted_assignments:
        # Exclude 'id' fields as requested
        title = assignment.get("title", "N/A")
        organization = assignment.get("organization", "N/A")
        location = assignment.get("location", "")
        date_range = assignment.get("date_range", "") # Already formatted in JSON

        # Format as H3 for title
        md_parts.append(f"### {title}")

        # Format organization | location | date_range as italicized
        org_loc_date_line = f"_{organization}"
        if location:
            org_loc_date_line += f" | {location}"
        if date_range:
            org_loc_date_line += f" | {date_range}"
        org_loc_date_line += "_"
        md_parts.append(org_loc_date_line)

        # Use 'tasks' for bullet points. If 'tasks' is not available, fall back to 'description'.
        tasks_content = assignment.get("tasks")
        if tasks_content:
            # Split tasks by newline and format as list items
            raw_tasks = [t.strip() for t in tasks_content.split('\n') if t.strip()]
            task_bullets = []
            for task in raw_tasks:
                # NEW: Remove any existing Markdown list markers (like *, -, +, or numbers followed by .)
                # before adding our own "* " to ensure clean bullet points.
                cleaned_task = re.sub(r"^\s*[-*+]\s*|^(\d+\.)\s*", "", task).strip()
                if cleaned_task: # Ensure it's not empty after cleaning
                    task_bullets.append(f"* {cleaned_task}")
            md_parts.extend(task_bullets)
        elif assignment.get("description"):
            # If no specific tasks, use the general description as a single bullet or paragraph
            md_parts.append(f"* {assignment['description'].strip()}")
        
        md_parts.append("") # Add a blank line for spacing between assignments

    return "\n".join(md_parts)


def build_master_skills_md(cv_data: dict) -> str:
    """
    Builds a comprehensive 'Key Skills & Tools' section by extracting unique skills
    from assignments' sectors and methodologies, and other relevant fields.
    This is a more exhaustive list for a master CV.
    """
    all_skills = set()

    # Extract from assignments
    for assignment in cv_data.get("assignments", []):
        for sector in assignment.get("sectors", []):
            all_skills.add(sector.strip())
        for method in assignment.get("methodologies", []):
            all_skills.add(method.strip())
        # You might also want to parse 'tasks' or 'description' for keywords
        # For now, let's stick to explicit lists to avoid hallucination

    # Add skills from certifications if they imply specific tools/skills
    for cert in cv_data.get("certifications", []):
        cert_name = cert.get("certification_name", "").lower()
        if "power bi" in cert_name:
            all_skills.add("Power BI")
        if "microsoft certified" in cert_name or "data analyst" in cert_name:
            all_skills.add("Data Analysis")
            all_skills.add("Microsoft Technologies")
        # Add more rules here as needed based on your certifications

    # Add skills from education if relevant (e.g., specific software, fields of study)
    for edu in cv_data.get("education", []):
        field_of_study = edu.get("field_of_study", "").lower()
        if "information systems" in field_of_study:
            all_skills.add("Information Systems")
        if "economics" in field_of_study:
            all_skills.add("Economic Analysis")
        # Add more rules here

    # Add specific tools/software if you want them to always appear
    # This is a good place to manually add skills that aren't easily inferred
    # from your structured data but you want to ensure are always present.
    # For example, from your sample CV:
    explicit_tools = [
        "SPSS", "Stata", "ATLAS.ti", "R", "EPI Info", "KoboToolbox", "Power BI",
        "Excel", "Google Sheets", "Google Docs", "Word", "NVivo" 
    ]
    for tool in explicit_tools:
        all_skills.add(tool)

    # Convert to a list and sort alphabetically for consistent output
    sorted_skills = sorted(list(all_skills))

    if not sorted_skills:
        return "## Key Skills & Tools\n*No key skills or tools listed.*"

    md_parts = ["## Key Skills & Tools", ""]
    for skill in sorted_skills:
        md_parts.append(f"* {skill}")
    return "\n".join(md_parts)


def generate_master_cv_markdown(cv_data: dict) -> str | None:
    """
    Generates a comprehensive master CV in Markdown format from the master CV JSON data.
    """
    log_info("Generating Master CV Markdown...")

    personal_md = build_personal_md(cv_data)
    education_md = build_education_md(cv_data.get("education"))
    certifications_md = build_certifications_md(cv_data.get("certifications"))
    publications_md = build_publications_md(cv_data.get("publications"))
    languages_md = build_languages_md(cv_data.get("languages"))
    
    # Build experience section from all assignments
    experience_md = build_master_experience_md(cv_data.get("assignments"))

    # Build comprehensive skills section
    skills_md = build_master_skills_md(cv_data)


    # Assemble all parts into the final Markdown string
    master_cv_markdown = (
        f"{personal_md}\n\n"
        f"{experience_md}\n\n"
        f"{skills_md}\n\n"
        f"{education_md}\n\n"
        f"{certifications_md}\n\n"
        f"{publications_md}\n\n"
        f"{languages_md}"
    )

    log_info("Master CV Markdown generated successfully.")
    return master_cv_markdown

if __name__ == "__main__":
    log_info("--- Master CV Markdown Generator Started ---")

    master_cv_data = read_master_cv_json()
    if not master_cv_data:
        log_error("Failed to read master CV data. Aborting master CV generation.")
    else:
        master_cv_md_content = generate_master_cv_markdown(master_cv_data)
        if master_cv_md_content:
            # Define output filename for the master CV
            output_filename = "master_cv_full.md"
            saved_filepath = save_text_to_output_dir(output_filename, master_cv_md_content)
            if saved_filepath:
                log_info(f"Master CV Markdown saved to: {saved_filepath}")
            else:
                log_error("Failed to save Master CV Markdown.")
        else:
            log_error("Failed to generate Master CV Markdown content.")

    log_info("--- Master CV Markdown Generator Finished ---")