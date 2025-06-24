# File: kazi/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROMPTS_DIR = os.path.join(PROJECT_ROOT, "prompts", "templates")
JD_STORAGE_DIR = os.path.join(PROJECT_ROOT, "jd_storage")
TOR_STORAGE_DIR = os.path.join(PROJECT_ROOT, "tor_storage") # NEW: Directory for TOR PDFs
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
CV_DATA_DIR = os.path.join(PROJECT_ROOT, "cv_data")
MASTER_CV_FILENAME = "master_cv.json"

# --- Google Docs API Settings (Disabled) ---
ENABLE_GOOGLE_DOCS_UPLOAD = False # Set to False to disable Google Docs upload

# Define the list of LLM models to iterate through and their specific settings
LLM_MODEL_CONFIGS = {
    # "gemini-1.5-flash-latest": {"max_output_tokens": 8192, "temperature": 0.7},
    # "gemini-2.0-flash": {"max_output_tokens": 8192, "temperature": 0.7},
    "gemini-2.5-flash-preview-05-20": {"max_output_tokens": 65536, "temperature": 0.7},
    # "gemini-2.5-pro-preview-05-06": {"max_output_tokens": 65536, "temperature": 1}
}

# Define the order of models to iterate, ensuring they exist in LLM_MODEL_CONFIGS
LLM_MODELS_TO_RUN = [
    # "gemini-1.5-flash-latest",
    # "gemini-2.0-flash",
    "gemini-2.5-flash-preview-05-20",
    # "gemini-2.5-pro-preview-05-06"
]

# Initialize LLM_MODEL_NAME with the first model from the run list
# This variable will be set dynamically by run.py for the current model being processed
LLM_MODEL_NAME = LLM_MODELS_TO_RUN[0] if LLM_MODELS_TO_RUN else "gemini-2.5-pro-preview-05-06"

# Dynamically set LLM_TEMPERATURE and LLM_MAX_OUTPUT_TOKENS based on LLM_MODEL_NAME
# These will be updated by run.py as it iterates through LLM_MODELS_TO_RUN
LLM_TEMPERATURE = LLM_MODEL_CONFIGS.get(LLM_MODEL_NAME, {}).get("temperature", 0.7)
LLM_MAX_OUTPUT_TOKENS = LLM_MODEL_CONFIGS.get(LLM_MODEL_NAME, {}).get("max_output_tokens", 8192)

def log_error(message):
    print(f"ERROR: {message}")

def log_info(message):
    print(f"INFO: {message}")

# Ensure all necessary directories exist
for dir_path in [OUTPUT_DIR, JD_STORAGE_DIR, TOR_STORAGE_DIR, CV_DATA_DIR, os.path.join(PROJECT_ROOT, "config")]:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        log_info(f"Created directory: {dir_path}")

if not os.path.exists(os.path.join(CV_DATA_DIR, MASTER_CV_FILENAME)):
    log_info(f"Master CV file not found at {os.path.join(CV_DATA_DIR, MASTER_CV_FILENAME)}. Please create it.")

