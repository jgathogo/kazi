# File: kazi/core/orchestrator.py
# Content:
import json # Ensure json is imported at the top
from core.jd_analyzer import analyze_job_description
from core.jd_cv_mapper import generate_jd_cv_mapping
from core.tor_analyzer import analyze_terms_of_reference
from core.document_generators.cv_generator import generate_tailored_experience_json, assemble_final_cv_markdown
from core.document_generators.cover_letter_generator import generate_cover_letter_markdown
from core.document_generators.technical_proposal_generator import generate_technical_approach_framework, generate_type_and_understanding_sections, generate_detailed_technical_approach_sections, generate_work_plan_and_deliverables_sections, generate_general_management_sections, generate_team_and_experience_sections, generate_executive_summary_section, assemble_technical_proposal_markdown # NEW: Import the assembly function
from core.content_synthesizer import generate_strategic_narrative
from data_management.input_handler import read_pdf_text_from_jd_storage, read_pdf_text_from_tor_storage, read_master_cv_json
from data_management.output_handler import save_text_to_output_dir
from config import settings
import os
import datetime
from core.document_generators.tailored_proposal_generator import (
    analyze_terms_of_reference_tailored,
    generate_customized_proposal_structure,
    generate_dynamic_section_content,
    assemble_customized_proposal_markdown
)


def run_full_application_package_pipeline(jd_pdf_filename: str) -> bool:
    settings.log_info(f"--- Starting Full Application Package Pipeline for: {jd_pdf_filename} ---")
    current_step_outputs = {} 
    base_jd_filename = os.path.splitext(os.path.basename(jd_pdf_filename))[0]

    timestamp = datetime.datetime.now().strftime("%H%M%d%m%y")
    settings.log_info(f"Generated timestamp for this run: {timestamp}")

    llm_model_suffix = settings.LLM_MODEL_NAME.replace("gemini-", "")
    settings.log_info(f"Using LLM Model: {settings.LLM_MODEL_NAME}")

    # --- Stage 1: JD Analysis (Prompt 1) ---
    settings.log_info("\nStage 1: Analyzing Job Description...")
    jd_text = read_pdf_text_from_jd_storage(jd_pdf_filename)
    if not jd_text:
        settings.log_error(f"Failed to read JD text from {jd_pdf_filename}. Aborting pipeline.")
        return False
    jd_analysis_markdown = analyze_job_description(jd_text)
    if not jd_analysis_markdown:
        settings.log_error("Failed to analyze job description (Prompt 1). Aborting pipeline.")
        return False
    current_step_outputs["jd_analysis_markdown"] = jd_analysis_markdown
    jd_analysis_output_filename = f"{base_jd_filename}_step1_jd_analysis_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(jd_analysis_output_filename, jd_analysis_markdown, base_file=base_jd_filename, app_type="job")
    settings.log_info(f"Stage 1: JD Analysis saved to output/{jd_analysis_output_filename}")

    # --- NEW Stage: JD-CV Mapping Generation ---
    settings.log_info("\nStage 1.5: Generating JD-CV Mapping (New Prompt)...")
    master_cv_data = read_master_cv_json()
    if not master_cv_data:
        settings.log_error("Failed to read master CV data. Aborting pipeline.")
        return False
    current_step_outputs["master_cv_data"] = master_cv_data # Store master_cv_data here as well
    jd_cv_mapping_json_str = generate_jd_cv_mapping(
        current_step_outputs["jd_analysis_markdown"],
        current_step_outputs["master_cv_data"]
    )
    if not jd_cv_mapping_json_str:
        settings.log_error("Failed to generate JD-CV mapping. Aborting pipeline.")
        return False
    current_step_outputs["jd_cv_mapping_json_str"] = jd_cv_mapping_json_str
    jd_cv_mapping_output_filename = f"{base_jd_filename}_step1_5_jd_cv_mapping_{timestamp}_{llm_model_suffix}.json"
    save_text_to_output_dir(jd_cv_mapping_output_filename, jd_cv_mapping_json_str, base_file=base_jd_filename, app_type="job")
    settings.log_info(f"Stage 1.5: JD-CV Mapping saved to output/{jd_cv_mapping_output_filename}")


    # --- Stage 2: Tailored Experience JSON (Prompt 2) ---
    # This stage will still run for CV generation, but Cover Letter will primarily use JD-CV Mapping now.
    settings.log_info("\nStage 2: Generating Tailored Experience JSON...")
    # master_cv_data is already loaded above
    tailored_experience_json_str = generate_tailored_experience_json(
        current_step_outputs["jd_analysis_markdown"], 
        current_step_outputs["master_cv_data"]
    )
    if not tailored_experience_json_str:
        settings.log_error("Failed to generate tailored experience JSON (Prompt 2). Aborting pipeline.")
        return False
    current_step_outputs["tailored_experience_json_str"] = tailored_experience_json_str
    tailored_exp_output_filename = f"{base_jd_filename}_step2_tailored_experience_{timestamp}_{llm_model_suffix}.json"
    save_text_to_output_dir(tailored_exp_output_filename, tailored_experience_json_str, base_file=base_jd_filename, app_type="job")
    settings.log_info(f"Stage 2: Tailored Experience JSON saved to output/{tailored_exp_output_filename}")

    # --- Stage 3: Strategic Narrative & Summary (Prompt 3) ---
    settings.log_info("\nStage 3: Generating Strategic Narrative & Professional Summary...")
    strategic_narrative_markdown = generate_strategic_narrative(
        current_step_outputs["jd_analysis_markdown"],
        current_step_outputs["tailored_experience_json_str"]
    )
    if not strategic_narrative_markdown:
        settings.log_error("Failed to generate strategic narrative (Prompt 3). Aborting pipeline.")
        return False
    current_step_outputs["strategic_narrative_markdown"] = strategic_narrative_markdown
    narrative_output_filename = f"{base_jd_filename}_step3_strategic_narrative_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(narrative_output_filename, strategic_narrative_markdown, base_file=base_jd_filename, app_type="job")
    settings.log_info(f"Stage 3: Strategic Narrative saved to output/{narrative_output_filename}")

    # --- Stage 4: Final CV Assembly (Prompt 4) ---
    settings.log_info("\nStage 4: Assembling Final CV Markdown...")
    final_cv_md = assemble_final_cv_markdown(
        current_step_outputs["jd_analysis_markdown"],
        current_step_outputs["tailored_experience_json_str"],
        current_step_outputs["strategic_narrative_markdown"],
        current_step_outputs["master_cv_data"] 
    )
    if not final_cv_md:
        settings.log_error("Failed to assemble final CV (Prompt 4). Aborting pipeline.")
        return False
    current_step_outputs["final_cv_md"] = final_cv_md
    final_cv_output_filename = f"{base_jd_filename}_step4_final_cv_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(final_cv_output_filename, final_cv_md, base_file=base_jd_filename, app_type="job")
    settings.log_info(f"Stage 4: Final CV Markdown saved to output/{final_cv_output_filename}")

    # --- Stage 5: Cover Letter Generation (Prompt 5) ---
    settings.log_info("\nStage 5: Generating Cover Letter...")
    cover_letter_md = generate_cover_letter_markdown(
        current_step_outputs["jd_analysis_markdown"],
        current_step_outputs["tailored_experience_json_str"], # Keeping for now, but Prompt 5 will primarily use mapping
        current_step_outputs["strategic_narrative_markdown"],
        current_step_outputs["master_cv_data"],
        current_step_outputs["jd_cv_mapping_json_str"] # NEW: Pass the mapping content
    )
    if not cover_letter_md:
        settings.log_error("Failed to generate Cover Letter (Prompt 5). Aborting pipeline.")
        return False
    current_step_outputs["cover_letter_md"] = cover_letter_md
    cover_letter_output_filename = f"{base_jd_filename}_step5_cover_letter_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(cover_letter_output_filename, cover_letter_md, base_file=base_jd_filename, app_type="job")
    settings.log_info(f"Stage 5: Cover Letter Markdown saved to output/{cover_letter_output_filename}")

    settings.log_info("\nGoogle Docs upload is disabled. Skipping Google Docs upload stages.")

    settings.log_info("\n--- Full Application Package Pipeline Completed Successfully ---")
    return True

# Keep the old function for now if you want to test only JD analysis
def run_jd_analysis_pipeline(jd_pdf_filename: str) -> str | None:
    settings.log_info(f"Starting JD analysis pipeline for: {jd_pdf_filename}")
    jd_text = read_pdf_text_from_jd_storage(jd_pdf_filename)
    if not jd_text:
        settings.log_error(f"Failed to read JD text from '{jd_pdf_filename}'. Aborting pipeline.")
        return None
    analysis_markdown = analyze_job_description(jd_text)
    if not analysis_markdown:
        settings.log_error("Failed to analyze job description. Aborting pipeline.")
        return None
    base_jd_filename = os.path.splitext(os.path.basename(jd_pdf_filename))[0]
    llm_model_suffix = settings.LLM_MODEL_NAME.replace("gemini-", "")
    timestamp = datetime.datetime.now().strftime("%H%M%d%m%y")
    output_filename = f"{base_jd_filename}_analysis_{timestamp}_{llm_model_suffix}.md" 
    saved_filepath = save_text_to_output_dir(output_filename, analysis_markdown, base_file=base_jd_filename, app_type="job")
    if saved_filepath:
        settings.log_info(f"JD analysis pipeline completed. Output saved to: {saved_filepath}")
    else:
        settings.log_error("Failed to save JD analysis.")
    return saved_filepath


def run_tor_analysis_pipeline(tor_pdf_filename: str) -> str | None:
    """
    Runs the pipeline for analyzing a Terms of Reference (ToR) document and generating
    initial technical proposal sections.
    """
    settings.log_info(f"--- Starting ToR Analysis and Initial Technical Proposal Sections Pipeline for: {tor_pdf_filename} ---")
    
    base_tor_filename = os.path.splitext(os.path.basename(tor_pdf_filename))[0]
    timestamp = datetime.datetime.now().strftime("%H%M%d%m%y")
    llm_model_suffix = settings.LLM_MODEL_NAME.replace("gemini-", "")

    current_step_outputs = {} # To store outputs for chaining within this pipeline

    # Stage 1: Read ToR PDF
    settings.log_info("\nStage 1: Reading ToR Document...")
    tor_text = read_pdf_text_from_tor_storage(tor_pdf_filename)
    if not tor_text:
        settings.log_error(f"Failed to read ToR text from {tor_pdf_filename}. Aborting pipeline.")
        return None

    # Stage 2: Analyze ToR (Prompt 6)
    settings.log_info("\nStage 2: Analyzing Terms of Reference (Prompt 6)...")
    tor_analysis_data = analyze_terms_of_reference(tor_text)
    if not tor_analysis_data:
        settings.log_error("Failed to analyze Terms of Reference (Prompt 6). Aborting pipeline.")
        return None
    current_step_outputs["tor_analysis_data"] = tor_analysis_data
    
    # Save the ToR analysis JSON
    tor_analysis_json_str = json.dumps(tor_analysis_data, indent=2)
    tor_analysis_output_filename = f"{base_tor_filename}_tor_analysis_{timestamp}_{llm_model_suffix}.json"
    save_text_to_output_dir(tor_analysis_output_filename, tor_analysis_json_str, base_file=base_tor_filename, app_type="consultancy")
    settings.log_info(f"Stage 2: ToR Analysis JSON saved to output/{tor_analysis_output_filename}")

    # --- Stage 3: Generate Type and Understanding of Assignment Sections (Prompt 8) ---
    settings.log_info("\nStage 3: Generating Type and Understanding of Assignment Sections (Prompt 8)...")
    type_and_understanding_md = generate_type_and_understanding_sections(
        current_step_outputs["tor_analysis_data"]
    )
    if not type_and_understanding_md:
        settings.log_error("Failed to generate Type and Understanding of Assignment sections (Prompt 8). Aborting pipeline.")
        return None
    current_step_outputs["type_and_understanding_md"] = type_and_understanding_md

    # Save the Markdown output for Sections 4 and 5
    type_understanding_output_filename = f"{base_tor_filename}_type_understanding_sections_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(type_understanding_output_filename, type_and_understanding_md, base_file=base_tor_filename, app_type="consultancy")
    settings.log_info(f"Stage 3: Type and Understanding of Assignment sections saved to output/{type_understanding_output_filename}")


    # --- Stage 4: Generate Technical Approach Framework (Prompt 7) ---
    settings.log_info("\nStage 4: Generating Technical Approach Framework (Prompt 7)...")
    technical_approach_framework = generate_technical_approach_framework(
        current_step_outputs["tor_analysis_data"]
    )
    if not technical_approach_framework:
        settings.log_error("Failed to generate Technical Approach Framework (Prompt 7). Aborting pipeline.")
        return None
    current_step_outputs["technical_approach_framework"] = technical_approach_framework

    # Save the Technical Approach Framework JSON
    framework_json_str = json.dumps(technical_approach_framework, indent=2)
    framework_output_filename = f"{base_tor_filename}_technical_approach_framework_{timestamp}_{llm_model_suffix}.json"
    save_text_to_output_dir(framework_output_filename, framework_json_str, base_file=base_tor_filename, app_type="consultancy")
    settings.log_info(f"Stage 4: Technical Approach Framework JSON saved to output/{framework_output_filename}")

    # --- Stage 5: Generate Detailed Technical Approach Sections (Prompt 9) ---
    settings.log_info("\nStage 5: Generating Detailed Technical Approach Sections (Prompt 9)...")
    detailed_technical_approach_md = generate_detailed_technical_approach_sections(
        current_step_outputs["tor_analysis_data"]
    )
    if not detailed_technical_approach_md:
        settings.log_error("Failed to generate Detailed Technical Approach sections (Prompt 9). Aborting pipeline.")
        return None
    current_step_outputs["detailed_technical_approach_md"] = detailed_technical_approach_md

    # Save the Markdown output for Sections 6.2 - 6.10
    detailed_tech_approach_output_filename = f"{base_tor_filename}_detailed_technical_approach_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(detailed_tech_approach_output_filename, detailed_technical_approach_md, base_file=base_tor_filename, app_type="consultancy")
    settings.log_info(f"Stage 5: Detailed Technical Approach sections saved to output/{detailed_tech_approach_output_filename}")

    # --- Stage 6: Generate Work Plan and Deliverables Sections (Prompt 10) ---
    settings.log_info("\nStage 6: Generating Work Plan and Deliverables Sections (Prompt 10)...")
    work_plan_deliverables_md = generate_work_plan_and_deliverables_sections(
        current_step_outputs["tor_analysis_data"]
    )
    if not work_plan_deliverables_md:
        settings.log_error("Failed to generate Work Plan and Deliverables sections (Prompt 10). Aborting pipeline.")
        return None
    current_step_outputs["work_plan_deliverables_md"] = work_plan_deliverables_md

    # Save the Markdown output for Section 7
    work_plan_deliverables_output_filename = f"{base_tor_filename}_work_plan_deliverables_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(work_plan_deliverables_output_filename, work_plan_deliverables_md, base_file=base_tor_filename, app_type="consultancy")
    settings.log_info(f"Stage 6: Work Plan and Deliverables sections saved to output/{work_plan_deliverables_output_filename}")

    # --- Stage 7: Generate General Management and Compliance Sections (Prompt 11) ---
    settings.log_info("\nStage 7: Generating General Management and Compliance Sections (Prompt 11)...")
    general_management_md = generate_general_management_sections(
        current_step_outputs["tor_analysis_data"]
    )
    if not general_management_md:
        settings.log_error("Failed to generate General Management and Compliance sections (Prompt 11). Aborting pipeline.")
        return None
    current_step_outputs["general_management_md"] = general_management_md

    # Save the Markdown output for Sections 10, 11, 12, 13
    general_management_output_filename = f"{base_tor_filename}_general_management_sections_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(general_management_output_filename, general_management_md, base_file=base_tor_filename, app_type="consultancy")
    settings.log_info(f"Stage 7: General Management and Compliance sections saved to output/{general_management_output_filename}")

    # --- Stage 8: Generate Team and Experience Sections (Prompt 12) ---
    settings.log_info("\nStage 8: Generating Team and Experience Sections (Prompt 12)...")
    master_cv_data = read_master_cv_json()
    if not master_cv_data:
        settings.log_error("Failed to read master CV data for team and experience sections. Aborting pipeline.")
        return None
    current_step_outputs["master_cv_data"] = master_cv_data

    team_and_experience_md = generate_team_and_experience_sections(
        current_step_outputs["tor_analysis_data"],
        current_step_outputs["master_cv_data"]
    )
    if not team_and_experience_md:
        settings.log_error("Failed to generate Team and Experience sections (Prompt 12). Aborting pipeline.")
        return None
    current_step_outputs["team_and_experience_md"] = team_and_experience_md

    # Save the Markdown output for Sections 8 and 9
    team_experience_output_filename = f"{base_tor_filename}_team_experience_sections_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(team_experience_output_filename, team_and_experience_md, base_file=base_tor_filename, app_type="consultancy")
    settings.log_info(f"Stage 8: Team and Experience sections saved to output/{team_experience_output_filename}")

    # --- Stage 9: Generate Executive Summary Section (Prompt 13) ---
    settings.log_info("\nStage 9: Generating Executive Summary Section (Prompt 13)...")
    executive_summary_md = generate_executive_summary_section(
        current_step_outputs["tor_analysis_data"],
        current_step_outputs["technical_approach_framework"], # JSON
        current_step_outputs["type_and_understanding_md"], # Markdown
        current_step_outputs["detailed_technical_approach_md"], # Markdown
        current_step_outputs["work_plan_deliverables_md"], # Markdown
        current_step_outputs["team_and_experience_md"], # Markdown
        current_step_outputs["general_management_md"] # Markdown
    )
    if not executive_summary_md:
        settings.log_error("Failed to generate Executive Summary section (Prompt 13). Aborting pipeline.")
        return None
    current_step_outputs["executive_summary_md"] = executive_summary_md

    # Save the Markdown output for Section 3
    executive_summary_output_filename = f"{base_tor_filename}_executive_summary_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(executive_summary_output_filename, executive_summary_md, base_file=base_tor_filename, app_type="consultancy")
    settings.log_info(f"Stage 9: Executive Summary section saved to output/{executive_summary_output_filename}")

    # --- Stage 10: Assemble Full Technical Proposal Markdown ---
    settings.log_info("\nStage 10: Assembling Full Technical Proposal Markdown...")
    full_proposal_md = assemble_technical_proposal_markdown(
        base_tor_filename=base_tor_filename,
        timestamp=timestamp,
        llm_model_suffix=llm_model_suffix,
        executive_summary_md=current_step_outputs["executive_summary_md"],
        type_and_understanding_md=current_step_outputs["type_and_understanding_md"],
        technical_approach_framework=current_step_outputs["technical_approach_framework"],
        detailed_technical_approach_md=current_step_outputs["detailed_technical_approach_md"],
        work_plan_deliverables_md=current_step_outputs["work_plan_deliverables_md"],
        team_and_experience_md=current_step_outputs["team_and_experience_md"],
        general_management_md=current_step_outputs["general_management_md"],
        master_cv_data=current_step_outputs["master_cv_data"] # Pass master_cv_data for cover page info
    )
    if not full_proposal_md:
        settings.log_error("Failed to assemble full technical proposal Markdown. Aborting pipeline.")
        return None

    # Save the consolidated Markdown output
    full_proposal_output_filename = f"{base_tor_filename}_full_technical_proposal_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(full_proposal_output_filename, full_proposal_md, base_file=base_tor_filename, app_type="consultancy")
    settings.log_info(f"Stage 10: Full Technical Proposal Markdown saved to output/{full_proposal_output_filename}")

    settings.log_info("\n--- ToR Analysis and Technical Proposal Sections Pipeline Completed Successfully ---")
    return full_proposal_md

def run_tor_analysis_tailored_pipeline(tor_pdf_filename: str) -> str | None:
    """
    Runs a tailored pipeline for analyzing ToR documents and generating customized proposals
    that adapt to the specific requirements rather than following a rigid template.
    """
    settings.log_info(f"--- Starting Tailored ToR Analysis and Customized Proposal Pipeline for: {tor_pdf_filename} ---")
    
    base_tor_filename = os.path.splitext(os.path.basename(tor_pdf_filename))[0]
    timestamp = datetime.datetime.now().strftime("%H%M%d%m%y")
    llm_model_suffix = settings.LLM_MODEL_NAME.replace("gemini-", "")

    current_step_outputs = {}

    # Stage 1: Read ToR PDF
    settings.log_info("\nStage 1: Reading ToR Document...")
    tor_text = read_pdf_text_from_tor_storage(tor_pdf_filename)
    if not tor_text:
        settings.log_error(f"Failed to read ToR text from {tor_pdf_filename}. Aborting pipeline.")
        return None

    # Stage 2: Tailored ToR Analysis
    settings.log_info("\nStage 2: Performing Tailored ToR Analysis...")
    tor_analysis_data = analyze_terms_of_reference_tailored(tor_text)
    if not tor_analysis_data:
        settings.log_error("Failed to perform tailored ToR analysis. Aborting pipeline.")
        return None
    current_step_outputs["tor_analysis_data"] = tor_analysis_data
    
    # Save the tailored ToR analysis JSON
    tor_analysis_json_str = json.dumps(tor_analysis_data, indent=2)
    tor_analysis_output_filename = f"{base_tor_filename}_tailored_tor_analysis_{timestamp}_{llm_model_suffix}.json"
    save_text_to_output_dir(tor_analysis_output_filename, tor_analysis_json_str, base_file=base_tor_filename, app_type="consultancy-tailored")
    settings.log_info(f"Stage 2: Tailored ToR Analysis JSON saved to output/{tor_analysis_output_filename}")

    # Stage 3: Generate Customized Proposal Structure
    settings.log_info("\nStage 3: Generating Customized Proposal Structure...")
    proposal_structure = generate_customized_proposal_structure(
        current_step_outputs["tor_analysis_data"]
    )
    if not proposal_structure:
        settings.log_error("Failed to generate customized proposal structure. Aborting pipeline.")
        return None
    current_step_outputs["proposal_structure"] = proposal_structure

    # Save the proposal structure JSON
    structure_json_str = json.dumps(proposal_structure, indent=2)
    structure_output_filename = f"{base_tor_filename}_customized_proposal_structure_{timestamp}_{llm_model_suffix}.json"
    save_text_to_output_dir(structure_output_filename, structure_json_str, base_file=base_tor_filename, app_type="consultancy-tailored")
    settings.log_info(f"Stage 3: Customized Proposal Structure saved to output/{structure_output_filename}")

    # Stage 4: Generate Dynamic Content for Each Section
    settings.log_info("\nStage 4: Generating Dynamic Content for Each Section...")
    master_cv_data = read_master_cv_json()
    if not master_cv_data:
        settings.log_error("Failed to read master CV data. Aborting pipeline.")
        return None
    current_step_outputs["master_cv_data"] = master_cv_data

    section_contents = {}
    for section in proposal_structure["proposal_structure"]["sections"]:
        settings.log_info(f"\nGenerating content for Section {section['section_number']}: {section['section_title']}...")
        
        section_content = generate_dynamic_section_content(
            current_step_outputs["tor_analysis_data"],
            current_step_outputs["proposal_structure"],
            section,
            current_step_outputs["master_cv_data"]
        )
        
        if not section_content:
            settings.log_error(f"Failed to generate content for section {section['section_title']}. Aborting pipeline.")
            return None
        
        section_contents[section['section_number']] = section_content
        
        # Save individual section content
        section_output_filename = f"{base_tor_filename}_section_{section['section_number']}_{section['section_title'].replace(' ', '_').lower()}_{timestamp}_{llm_model_suffix}.md"
        save_text_to_output_dir(section_output_filename, section_content, base_file=base_tor_filename, app_type="consultancy-tailored")
        settings.log_info(f"Section {section['section_number']} content saved to output/{section_output_filename}")

    current_step_outputs["section_contents"] = section_contents

    # Stage 5: Assemble Customized Proposal
    settings.log_info("\nStage 5: Assembling Customized Proposal...")
    full_proposal_md = assemble_customized_proposal_markdown(
        base_tor_filename=base_tor_filename,
        timestamp=timestamp,
        llm_model_suffix=llm_model_suffix,
        proposal_structure=current_step_outputs["proposal_structure"],
        section_contents=current_step_outputs["section_contents"],
        tor_analysis_data=current_step_outputs["tor_analysis_data"],
        master_cv_data=current_step_outputs["master_cv_data"]
    )
    
    if not full_proposal_md:
        settings.log_error("Failed to assemble customized proposal Markdown. Aborting pipeline.")
        return None

    # Save the customized proposal
    full_proposal_output_filename = f"{base_tor_filename}_customized_proposal_{timestamp}_{llm_model_suffix}.md"
    save_text_to_output_dir(full_proposal_output_filename, full_proposal_md, base_file=base_tor_filename, app_type="consultancy-tailored")
    settings.log_info(f"Stage 5: Customized Proposal saved to output/{full_proposal_output_filename}")

    settings.log_info("\n--- Tailored ToR Analysis and Customized Proposal Pipeline Completed Successfully ---")
    return full_proposal_md
