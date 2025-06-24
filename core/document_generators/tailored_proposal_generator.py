import json
from prompts.prompt_loader import load_prompt
from core.llm_interface import generate_text_from_prompt
from config import settings
from utils.text_utils import extract_json_from_response


def analyze_terms_of_reference_tailored(tor_text: str) -> dict | None:
    """
    Performs a tailored analysis of the ToR document, focusing on understanding
    the unique requirements and context rather than following a rigid template.
    """
    settings.log_info("Initiating Tailored ToR Analysis...")
    
    prompt_template = load_prompt("tor_analysis_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load tailored ToR analysis prompt template.")
        return None
    
    prompt = prompt_template.replace("{{tor_text}}", tor_text)
    
    response = generate_text_from_prompt(prompt)
    if not response:
        settings.log_error("Failed to receive response from LLM for tailored ToR analysis.")
        return None
    
    settings.log_info("Successfully received tailored ToR analysis from LLM.")
    
    # Extract JSON from response
    tor_analysis_json_str = extract_json_from_response(response)
    if not tor_analysis_json_str:
        settings.log_error("Failed to extract JSON from tailored ToR analysis response.")
        return None
    try:
        tor_analysis_data = json.loads(tor_analysis_json_str)
    except Exception as e:
        settings.log_error(f"Failed to parse tailored ToR analysis JSON: {e}")
        return None
    settings.log_info("Successfully extracted tailored ToR analysis JSON from LLM response.")
    return tor_analysis_data


def generate_customized_proposal_structure(tor_analysis_data: dict) -> dict | None:
    """
    Generates a customized proposal structure based on the tailored ToR analysis.
    """
    settings.log_info("Initiating Customized Proposal Structure Generation...")
    
    prompt_template = load_prompt("proposal_structure_generator_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load proposal structure generator prompt template.")
        return None
    
    tor_analysis_json = json.dumps(tor_analysis_data, indent=2)
    prompt = prompt_template.replace("{{tor_analysis_json}}", tor_analysis_json)
    
    response = generate_text_from_prompt(prompt)
    if not response:
        settings.log_error("Failed to receive response from LLM for proposal structure generation.")
        return None
    
    settings.log_info("Successfully received proposal structure from LLM.")
    
    # Extract JSON from response
    proposal_structure_json_str = extract_json_from_response(response)
    if not proposal_structure_json_str:
        settings.log_error("Failed to extract JSON from proposal structure response.")
        return None
    try:
        proposal_structure = json.loads(proposal_structure_json_str)
    except Exception as e:
        settings.log_error(f"Failed to parse proposal structure JSON: {e}")
        return None
    settings.log_info("Successfully extracted proposal structure JSON from LLM response.")
    return proposal_structure


def generate_dynamic_section_content(tor_analysis_data: dict, proposal_structure: dict, section: dict, master_cv_data: dict) -> str | None:
    """
    Generates dynamic content for a specific section based on the tailored analysis.
    """
    settings.log_info(f"Initiating Dynamic Content Generation for Section {section['section_number']}...")
    
    prompt_template = load_prompt("dynamic_content_generator_prompt.txt")
    if not prompt_template:
        settings.log_error("Failed to load dynamic content generator prompt template.")
        return None
    
    # Prepare the prompt with all necessary context
    tor_analysis_json = json.dumps(tor_analysis_data, indent=2)
    proposal_structure_json = json.dumps(proposal_structure, indent=2)
    master_cv_json = json.dumps(master_cv_data, indent=2)
    
    # Extract key context from tor_analysis_data
    assignment_essence = tor_analysis_data.get("assignment_essence", {})
    assignment_type = assignment_essence.get("type", "Unknown")
    client_context = assignment_essence.get("client_context", "Unknown")
    core_problem = assignment_essence.get("core_problem", "Unknown")
    
    prompt = prompt_template.replace("{{tor_analysis_json}}", tor_analysis_json)
    prompt = prompt.replace("{{proposal_structure_json}}", proposal_structure_json)
    prompt = prompt.replace("{{master_cv_data}}", master_cv_json)
    prompt = prompt.replace("{{assignment_type}}", assignment_type)
    prompt = prompt.replace("{{client_context}}", client_context)
    prompt = prompt.replace("{{core_problem}}", core_problem)
    prompt = prompt.replace("{{section_title}}", section.get("section_title", "Unknown"))
    prompt = prompt.replace("{{section_focus}}", section.get("content_focus", "Unknown"))
    
    response = generate_text_from_prompt(prompt)
    if not response:
        settings.log_error(f"Failed to receive response from LLM for section {section['section_title']}.")
        return None
    
    settings.log_info(f"Successfully received content for section {section['section_title']} from LLM.")
    return response


def assemble_customized_proposal_markdown(base_tor_filename: str, timestamp: str, llm_model_suffix: str, 
                                        proposal_structure: dict, section_contents: dict, 
                                        tor_analysis_data: dict, master_cv_data: dict) -> str | None:
    """
    Assembles the customized proposal from all generated sections.
    """
    settings.log_info("Initiating Customized Proposal Assembly...")
    
    try:
        # Start with the proposal title
        proposal_title = proposal_structure["proposal_structure"]["title"]
        
        # Build the proposal content
        proposal_content = f"# {proposal_title}\n\n"
        
        # Add executive summary if it exists
        if "1" in section_contents:
            proposal_content += f"## Executive Summary\n\n{section_contents['1']}\n\n"
        
        # Add all other sections in order
        sections = proposal_structure["proposal_structure"]["sections"]
        for section in sections:
            section_num = section["section_number"]
            if section_num in section_contents and section_num != "1":  # Skip exec summary as it's already added
                section_title = section["section_title"]
                proposal_content += f"## {section_title}\n\n{section_contents[section_num]}\n\n"
        
        # Add any unique elements
        unique_elements = proposal_structure["proposal_structure"].get("unique_elements", [])
        if unique_elements:
            proposal_content += "## Additional Elements\n\n"
            for element in unique_elements:
                proposal_content += f"### {element}\n\n"
        
        settings.log_info("Customized Proposal Assembly completed.")
        return proposal_content
        
    except Exception as e:
        settings.log_error(f"Error assembling customized proposal: {str(e)}")
        return None 