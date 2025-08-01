# File: kazi/run.py
# Content:
import argparse
from core.orchestrator import run_full_application_package_pipeline, run_tor_analysis_pipeline, run_tor_analysis_tailored_pipeline
from config import settings
import os
import time

def main():
    parser = argparse.ArgumentParser(description="Kazi: AI-powered Document Generator CLI")
    parser.add_argument(
        "input_filename", 
        type=str, 
        help="Filename of the input PDF (Job Description or Terms of Reference). The script expects this file to be in 'jd_storage' for 'job' type or 'tor_storage' for 'consultancy' type."
    )
    parser.add_argument(
        "--type",
        type=str,
        choices=["job", "consultancy", "consultancy-tailored"],  # <-- Add "consultancy-tailored" here
        default="job",
        help="Type of application to generate: 'job' for CV/Cover Letter, 'consultancy' for generic ToR analysis, 'consultancy-tailored' for dynamic, customized proposals."
    )
    parser.add_argument(
        "--consultant-email",
        default="james@gathogo.co.ke",
        help="The email of the consultant whose profile should be used for generation. Defaults to 'james@gathogo.co.ke'."
    )
    args = parser.parse_args()

    # Inform the user if the default email is being used for a job application.
    if args.type == "job" and args.consultant_email == "james@gathogo.co.ke":
        settings.log_info(f"Using default consultant email for job application: {args.consultant_email}")

    settings.log_info(f"--- Kazi CLI Started for {args.type.upper()} Application ---")

    if not settings.GOOGLE_API_KEY: # For Gemini API
        settings.log_error("GOOGLE_API_KEY for Gemini is not configured. Please check your .env file.")
        settings.log_info("--- Kazi CLI Finished (with errors) ---")
        return

    # Determine the correct storage directory based on the application type
    storage_dir = ""
    if args.type == "job":
        storage_dir = settings.JD_STORAGE_DIR
    elif args.type in ["consultancy", "consultancy-tailored"]:
        storage_dir = settings.TOR_STORAGE_DIR

    # Validate the input file path
    input_file_path = os.path.join(storage_dir, os.path.basename(args.input_filename))
    if not os.path.exists(input_file_path):
        settings.log_error(f"The specified file '{os.path.basename(args.input_filename)}' was not found in '{storage_dir}'.")
        settings.log_info("--- Kazi CLI Finished (with errors) ---")
        return

    # Generate a timestamp for the output directory
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    all_success = True
    for model_name in settings.LLM_MODELS_TO_RUN:
        settings.log_info(f"\n--- Starting Pipeline for model: {model_name} ---")
        settings.LLM_MODEL_NAME = model_name # Set the current model for this specific run
        
        success = False
        if args.type == "job":
            success = run_full_application_package_pipeline(args.input_filename, args.consultant_email, timestamp)
        elif args.type == "consultancy":
            result = run_tor_analysis_pipeline(args.input_filename, args.consultant_email, timestamp)
            success = result is not None # Success if analysis data is returned
        elif args.type == "consultancy-tailored":
            result = run_tor_analysis_tailored_pipeline(args.input_filename, timestamp)  # Pass timestamp
            success = result is not None  # Success if result is not None

        if success:
            print(f"\nSUCCESS: {args.type.upper()} pipeline complete for model {model_name}. Check the 'output' directory.")
        else:
            print(f"\nERROR: {args.type.upper()} pipeline failed for model {model_name}. Please check the logs above for details.")
            all_success = False
        
        # Add a delay between runs, unless it's the last model
        if settings.LLM_MODELS_TO_RUN.index(model_name) < len(settings.LLM_MODELS_TO_RUN) - 1:
            delay_seconds = 5 # You can change this value for a longer/shorter pause
            settings.log_info(f"Pausing for {delay_seconds} seconds before running with the next model...")
            time.sleep(delay_seconds)

    if all_success:
        settings.log_info(f"\n--- All {args.type.upper()} Pipelines Completed Successfully ---")
    else:
        settings.log_error(f"\n--- One or more {args.type.upper()} Pipelines Failed ---")
    
    settings.log_info("--- Kazi CLI Finished ---")

if __name__ == "__main__":
    main()
