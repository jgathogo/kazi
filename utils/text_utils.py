# File: kazi/utils/text_utils.py
# Create this new file
import re
import json
from config import settings

def extract_json_from_response(text: str) -> str | None:
    """
    Extracts a JSON block from a text response, typically from an LLM.
    Handles JSON fenced with ```json ... ``` or if the entire response is JSON.
    Args:
        text: The text containing the JSON block.
    Returns:
        The extracted JSON string, or None if no valid JSON block is found.
    """
    if not text:
        return None
    
    # Regex to find JSON block, case-insensitive, allowing for optional "json" language specifier
    # It looks for ``` followed by optional "json" and newline, then captures content, then ```
    match = re.search(r"```(?:json)?\s*(\{[\s\S]*\}|\[[\s\S]*\])\s*```", text, re.IGNORECASE | re.DOTALL)
    
    if match:
        json_block = match.group(1).strip()
        try:
            # Validate if the extracted block is valid JSON
            json.loads(json_block)
            settings.log_info("Successfully extracted and validated JSON block from LLM response.")
            return json_block
        except json.JSONDecodeError as e:
            settings.log_error(f"Found JSON block but failed to parse. Error: {e}")
            settings.log_error(f"Problematic JSON block snippet: {json_block[:500]}...")
            return None # Or you could return the block and let the caller handle the parse error
    else:
        # If no ```json block, try to parse the whole text as JSON
        # This handles cases where the LLM might return raw JSON without fencing
        try:
            json_data = json.loads(text.strip())
            # If it's a list or dict, it's likely the intended JSON
            if isinstance(json_data, (dict, list)):
                 settings.log_info("No ```json block, but entire response is valid JSON.")
                 return text.strip()
        except json.JSONDecodeError:
            settings.log_error("No ```json block found and the whole text is not valid JSON.")
            return None
    return None