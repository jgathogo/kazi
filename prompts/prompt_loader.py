# File: kazi/prompts/prompt_loader.py
# Content:
import os
from config import settings

def load_prompt(prompt_name: str) -> str | None:
    """
    Loads a specific prompt template from the templates directory.
    Args:
        prompt_name: The filename of the prompt template.
    Returns:
        The content of the prompt template as a string, or None if not found.
    """
    prompt_path = "" 

    if prompt_name == "jd_analysis_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "common", prompt_name)
    elif prompt_name == "cv_tailoring_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "cv", prompt_name)
    elif prompt_name == "summary_generation_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "common", prompt_name)
    elif prompt_name == "cv_assembly_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "cv", prompt_name)
    elif prompt_name == "cover_letter_generation_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "cover_letter", prompt_name)
    elif prompt_name == "tor_analysis_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "consultancy", prompt_name)
    elif prompt_name == "technical_approach_framework_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "consultancy", prompt_name)
    elif prompt_name == "understanding_assignment_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "consultancy", prompt_name)
    elif prompt_name == "technical_approach_details_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "consultancy", prompt_name)
    elif prompt_name == "work_plan_deliverables_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "consultancy", prompt_name)
    elif prompt_name == "general_management_sections_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "consultancy", prompt_name)
    elif prompt_name == "team_and_experience_sections_prompt.txt":
        prompt_path = os.path.join(settings.PROMPTS_DIR, "consultancy", prompt_name)
    elif prompt_name == "executive_summary_prompt.txt": # NEW: For Executive Summary
        prompt_path = os.path.join(settings.PROMPTS_DIR, "consultancy", prompt_name)
    elif prompt_name == "jd_cv_mapping_prompt.txt": # NEW
        prompt_path = os.path.join(settings.PROMPTS_DIR, "common", prompt_name)
    elif prompt_name in [
        "tor_analysis_prompt.txt",
        "proposal_structure_generator_prompt.txt",
        "dynamic_content_generator_prompt.txt"
    ] and os.path.exists(os.path.join(settings.PROMPTS_DIR, "consultancy-tailored", prompt_name)):
        prompt_path = os.path.join(settings.PROMPTS_DIR, "consultancy-tailored", prompt_name)
    else:
        settings.log_error(f"Prompt '{prompt_name}' path not defined in prompt_loader yet.")
        return None

    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
        settings.log_info(f"Successfully loaded prompt: {prompt_path}")
        return prompt_content
    except FileNotFoundError:
        settings.log_error(f"Prompt file not found at: {prompt_path}")
        return None
    except Exception as e:
        settings.log_error(f"Error loading prompt {prompt_path}: {e}")
        return None
