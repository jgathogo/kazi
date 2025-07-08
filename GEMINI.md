# Kazi Project - Gemini AI Agent Notes

This `GEMINI.md` file serves as a project-specific knowledge base for the Gemini AI agent, documenting key aspects of the Kazi codebase and operational guidelines.

## 1. Project Overview

Kazi is a sophisticated Python-based system designed to automate the generation of tailored job application materials. It analyzes Job Descriptions (JDs) or Terms of Reference (ToRs) and, using Large Language Models (LLMs), produces customized CVs, cover letters, and detailed technical proposals.

## 2. Key Technologies

*   **Language:** Python
*   **LLM Integration:** Utilizes Google Gemini API (via `langchain` and `google-generativeai` libraries as per `requirements.txt`).
*   **PDF Processing:** `pdfminer.six` for extracting text from PDF documents.
*   **Configuration:** `config/settings.py` for application-wide settings.

## 3. Core Workflows & Pipelines

The project features distinct pipelines for different application types:

*   **`job` pipeline:** Generates tailored CVs and cover letters based on JDs.
*   **`consultancy` pipeline:** Performs generic ToR analysis and generates initial technical proposal sections.
*   **`consultancy-tailored` pipeline:** (Focus of recent interactions) Dynamically analyzes ToRs, generates customized proposal structures, and creates tailored content for each section.

## 4. Recent Interactions & Code Changes

During recent interactions, the following significant changes were implemented to enhance the `consultancy-tailored` pipeline:

### 4.1. Prompt Engineering Enhancements

The three core prompts in `prompts/templates/consultancy-tailored/` were significantly refined:

*   **`tor_analysis_prompt.txt`**: 
    *   Added `CRITICAL INSTRUCTIONS` for strict JSON output adherence (no extra fields, internal validation).
    *   **New Feature:** Introduced an `audience_profile` section to the JSON schema, instructing the LLM to deduce the likely readers, their priorities, technical level, and decision-making drivers directly from the ToR.
*   **`proposal_structure_generator_prompt.txt`**: 
    *   Added `CRITICAL INSTRUCTIONS` to explicitly forbid generic sections and to use the `audience_profile` for strategic section definition.
    *   **New Feature:** Added a `persuasive_angle` field to each section within the JSON schema, guiding the LLM to define the key persuasive goal for that section based on the identified audience.
*   **`dynamic_content_generator_prompt.txt`**: 
    *   Updated `Persona` to be a "strategic communicator and expert storyteller."
    *   **New Feature:** Replaced static audience awareness with a dynamic `Audience Profile` section, populated from the `tor_analysis_json`.
    *   Refined `What to Avoid` and `Tone and Style` sections to emphasize clarity, conciseness, client-centricity, benefit-orientation, and relatability for a mixed business audience.

### 4.2. Flexible File Input

*   **`data_management/input_handler.py`**: Modified `read_pdf_text` to `read_file_text` to support reading both `.pdf` and `.txt` files. This involved adding logic to check file extensions and use `pdfminer` for PDFs or standard file reading for text files.
*   **`core/orchestrator.py`**: Updated all calls to `read_pdf_text_from_jd_storage` and `read_pdf_text_from_tor_storage` to use the new `read_text_from_jd_storage` and `read_text_from_tor_storage` functions respectively.

### 4.3. Filename Sanitization

*   **`core/orchestrator.py`**: 
    *   Added a `sanitize_filename` helper function to remove invalid characters (e.g., `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) from strings.
    *   Implemented this `sanitize_filename` function when generating output filenames for individual sections within the `consultancy-tailored` pipeline to prevent `FileNotFoundError` due to invalid characters.

### 4.4. Timestamped Output Directories

*   **`core/orchestrator.py`**: Modified the `run_tor_analysis_tailored_pipeline` function to create a unique, timestamped subdirectory for each run within the `output/consultancy-tailored/` path. This helps in organizing and comparing different iterations of generated proposals. The format is `[base_tor_filename]_[YYYYMMDD_HHMMSS]`.

## 5. Running Tests

To run the `consultancy-tailored` pipeline with a specific TOR file (e.g., `gate_jul_25.txt` located in `tor_storage/`), use the following command from the project root:

```bash
python run.py gate_jul_25.txt --type consultancy-tailored
```

Output will be saved in a timestamped folder under `output/consultancy-tailored/`.

## 6. Agent Operational Guidelines

*   **File Visibility:** This agent is aware that `tor_storage/` and other data directories contain files that are intentionally ignored by `.gitignore`. When listing or searching these directories, the agent will use `respect_git_ignore=False` in its tool calls to ensure all files are visible for operational purposes, unless explicitly instructed otherwise.

```