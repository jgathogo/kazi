# In file: kazi-main/utils/markdown_formatter.py

import re
import os

def format_markdown_file(file_path):
    """
    Reads a markdown file, fixes common and complex formatting errors,
    and overwrites the file with the corrected content.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Apply Formatting Rules ---

    # Rule 1: Ensure headings have a blank line after them for spacing.
    content = re.sub(r'(\n#+ .+\n)(?!\n)', r'\1\n', content)

    # NEW Rule 2: Add a blank line before a list that follows a non-list line (like a heading or text).
    # This prevents lists from being attached directly to the line above them.
    content = re.sub(r'(:[^\n]+)\n(\s*\*|\s*-)', r'\1\n\n\2', content)


    # Rule 3: Re-process lists to fix sub-bullet indentation and add spacing.
    formatted_lines = []
    in_experience_section = False
    for line in content.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith('## Experience'):
            in_experience_section = True
        elif stripped_line.startswith('## '): # Exiting the Experience section
            in_experience_section = False

        # Fix for sub-bullets in the "Experience" section
        if in_experience_section and stripped_line.startswith('*'):
            # This identifies the primary bullet (the job role) by the pipe '|' character
            if '|' in stripped_line:
                # Add the primary bullet line as it is
                formatted_lines.append(line)
                # NEW: Add a blank line immediately after it for spacing
                formatted_lines.append("")
                continue # Move to the next line
            else: # This is an achievement sub-bullet
                # Indent the achievement to make it a properly nested sub-bullet
                formatted_lines.append(f"    * {stripped_line.lstrip('* ').strip()}")
                continue

        # Fix for malformed publications list
        if stripped_line.startswith('Click on each title to access the document'):
            parts = [p.strip() for p in stripped_line.split('-') if p.strip()]
            pub_items = parts[1:]
            formatted_lines.append("_Click on each title to access the document – most are hosted on client websites_")
            for item in pub_items:
                formatted_lines.append(f"- {item}")
            continue

        formatted_lines.append(line)

    content = '\n'.join(formatted_lines)

    # Overwrite the original file with the cleaned-up content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Markdown file formatted successfully: {file_path}")