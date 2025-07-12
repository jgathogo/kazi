# Kazi Project - Gemini AI Agent Notes

This `GEMINI.md` file serves as a project-specific knowledge base for the Gemini AI agent, documenting key aspects of the Kazi codebase and operational guidelines.

## 1. Project Overview

Kazi is a sophisticated Python-based system designed to automate the generation of tailored job application materials. It analyzes Job Descriptions (JDs) or Terms of Reference (ToRs) and, using Large Language Models (LLMs), produces customized CVs, cover letters, and detailed technical proposals.

## 2. Key Technologies

*   **Language:** Python
*   **LLM Integration:** Utilizes Google Gemini API (via `langchain` and `google-generativeai` libraries as per `requirements.txt`).
*   **PDF Processing:** `pdfminer.six` for extracting text from PDF files.
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
*   **`core/orchestrator.py`**: Updated all calls to `read_pdf_text_from_jd_storage` and `read_text_from_tor_storage` to use the new `read_text_from_jd_storage` and `read_text_from_tor_storage` functions respectively.

### 4.3. Filename Sanitization

*   **`core/orchestrator.py`**: 
    *   Added a `sanitize_filename` helper function to remove invalid characters (e.g., `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>`, `|`) from strings.
    *   Implemented this `sanitize_filename` function when generating output filenames for individual sections within the `consultancy-tailored` pipeline to prevent `FileNotFoundError` due to invalid characters.

### 4.4. Timestamped Output Directories

*   **`core/orchestrator.py`**: Modified the `run_tor_analysis_tailored_pipeline` function to create a unique, timestamped subdirectory for each run within the `output/consultancy-tailored/` path. This helps in organizing and comparing different iterations of generated proposals. The format is `[base_tor_filename]_[YYYYMMDD_HHMMSS]`.

### 4.5. Database Integration & Troubleshooting

**Problem:** The project migrated from using `master_cv.json` for consultant data to a MySQL database (`kazi_db`). This introduced `ModuleNotFoundError` and database connection issues when `data_management/db_handler.py` attempted to interact with the database.

**Initial Approach (Django ORM):** Attempts were made to configure Django's ORM within the `db_handler.py` to correctly connect to the database. This involved:
*   Correcting `DJANGO_SETTINGS_MODULE` path (`datastore.datastore.settings` then `datastore.settings`).
*   Adding `datastore` directory to `sys.path`.
*   Ensuring `__init__.py` existed in `datastore/`.
*   Moving Django setup to `run.py` (later reverted).

**Resolution (Direct MySQL Connection):** Due to persistent and complex Django ORM setup issues in a non-Django application context, the approach was shifted to direct MySQL database interaction.
*   **`data_management/db_handler.py` was completely rewritten:**
    *   Removed all Django ORM dependencies and setup code.
    *   Now uses `MySQLdb` (the Python module for `mysqlclient`) for direct database connection.
    *   All data retrieval is performed using raw SQL queries.
    *   Error handling for `MySQLdb.Error` was implemented.
    *   Removed `is_connected()` check from `finally` block as it's not supported by `MySQLdb`.
*   **`core/orchestrator.py`:**
    *   Imported `save_text_to_output_dir` from `data_management.output_handler` to resolve a `NameError`.
    *   Implemented `check_db_connection()` to perform a pre-check for database connectivity, aborting the pipeline early if the connection fails.
    *   Implemented `select_team_for_proposal()` to allow interactive selection of firms and individual consultants from the database.

**Current Status:** The `consultancy-tailored` pipeline now runs successfully end-to-end, including interactive team selection and database integration via direct MySQL queries. The selected firm and consultant information is now correctly displayed in the generated proposal, and the LLM is effectively incorporating relevant team expertise into the narrative sections.

## 5. Running Tests

To run the `consultancy-tailored` pipeline with a specific TOR file (e.g., `gate_jul_25.pdf` located in `tor_storage/`), use the following command from the project root:

```bash
python run.py gate_jul_25.pdf --type consultancy-tailored
```

Output will be saved in a timestamped folder under `output/consultancy-tailored/`.

## 6. Agent Operational Guidelines

*   **File Visibility:** This agent is aware that `tor_storage/` and other data directories contain files that are intentionally ignored by `.gitignore`. When listing or searching these directories, the agent will use `respect_git_ignore=False` in its tool calls to ensure all files are visible for operational purposes, unless explicitly instructed otherwise.