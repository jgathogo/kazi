# File: kazi/core/llm_interface.py
# Content:
import google.generativeai as genai
from config import settings # Import settings from the config package

def configure_llm():
    """Configures the generative AI model."""
    if not settings.GOOGLE_API_KEY:
        settings.log_error("GOOGLE_API_KEY is not set in .env file or environment variables.")
        raise ValueError("GOOGLE_API_KEY is missing.")
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    settings.log_info("Google Generative AI configured.")

def generate_text_from_prompt(prompt_text: str,
                              model_name: str = settings.LLM_MODEL_NAME,
                              temperature: float = settings.LLM_TEMPERATURE,
                              max_output_tokens: int = settings.LLM_MAX_OUTPUT_TOKENS
                              ) -> str | None:
    """
    Sends a prompt to the configured LLM and returns the generated text.
    Args:
        prompt_text: The complete prompt string.
        model_name: The name of the model to use.
        temperature: The temperature for generation.
        max_output_tokens: The maximum number of tokens for the output.
    Returns:
        The LLM's response text, or None if an error occurs.
    """
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens
            }
        )
        # For simplicity, not using chat history for this single-turn JD analysis yet.
        # If complex multi-turn conversations are needed later, this should be adapted.
        response = model.generate_content(prompt_text)
        settings.log_info(f"Successfully received response from LLM model {model_name}.")
        return response.text
    except Exception as e:
        settings.log_error(f"Error generating text with LLM model {model_name}: {e}")
        # You might want to inspect response.prompt_feedback here for safety ratings etc.
        # For example: if response.prompt_feedback.block_reason: log_error(...)
        return None

# Call configure_llm() when this module is imported so it's ready to use.
# However, it's often better to call configuration explicitly at the start of your app (e.g., in run.py or orchestrator).
# For now, let's keep it simple. If issues arise, we can move it.
try:
    configure_llm()
except ValueError as e:
    # This error will be logged by configure_llm itself.
    # We might want to re-raise or handle it more gracefully in an application context.
    pass