# In file: kazi-main/utils/convert_md_to_pdf.py

import os
import argparse
from weasyprint import HTML
import markdown

# Step 1: Import the new formatter function from the adjacent utility script
try:
    from .markdown_formatter import format_markdown_file
except ImportError:
    # This allows the script to be run directly for testing, assuming markdown_formatter.py is in the same directory
    from markdown_formatter import format_markdown_file

def convert_md_to_pdf(md_filepath: str, css_filepath: str | None = None) -> str | None:
    """
    Converts a Markdown file to a PDF file after first cleaning and formatting
    the Markdown content.

    Args:
        md_filepath: The absolute or relative path to the input Markdown file.
        css_filepath: Optional. The path to the CSS stylesheet. If not provided,
                      it defaults to 'resume_markdown_pdf_style.css' in the script's directory.

    Returns:
        The full path to the generated PDF file, or None if an error occurs.
    """
    script_directory = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.abspath(md_filepath)

    if not os.path.exists(md_path):
        print(f"ERROR: Markdown file not found at: {md_path}")
        return None

    # --- NEW: Call the formatter to clean the markdown file in place ---
    print(f"INFO: Formatting Markdown file: {md_path}")
    format_markdown_file(md_path)
    # --------------------------------------------------------------------

    # Determine CSS path
    stylesheets_to_load = []
    # Use the provided CSS file, or default to the one you uploaded
    css_path_to_use = css_filepath if css_filepath else os.path.join(script_directory, "resume_markdown_pdf_style.css")
    
    if os.path.exists(css_path_to_use):
        stylesheets_to_load.append(css_path_to_use)
        print(f"INFO: Using CSS stylesheet at: {css_path_to_use}")
    else:
        print(f"WARNING: CSS file not found at: {css_path_to_use}. PDF will have basic styling.")

    # Define output PDF path
    pdf_file_name = os.path.splitext(os.path.basename(md_path))[0] + ".pdf"
    pdf_path = os.path.join(os.path.dirname(md_path), pdf_file_name)

    print(f"INFO: Reading formatted Markdown from: {md_path}")
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()
    except Exception as e:
        print(f"ERROR: Could not read Markdown file {md_path}: {e}")
        return None

    print("INFO: Converting Markdown to HTML...")
    # Using 'markdown' library for conversion
    html_body = markdown.markdown(md_text, extensions=['fenced_code', 'tables', 'toc'])

    # Create a full HTML document structure to link the stylesheet
    html_full = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Converted PDF</title>
</head>
<body>
    {html_body}
</body>
</html>"""

    print(f"INFO: Converting HTML to PDF, saving to: {pdf_path}")
    try:
        # Pass the HTML string and stylesheets to WeasyPrint
        HTML(string=html_full, base_url=os.path.dirname(md_path)).write_pdf(
            pdf_path,
            stylesheets=stylesheets_to_load
        )
        print(f"SUCCESS: PDF created successfully: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"ERROR: An error occurred during PDF conversion: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a Markdown file to PDF after auto-formatting.")
    parser.add_argument("markdown_file", type=str, help="Path to the Markdown file.")
    parser.add_argument("--css", type=str, help="Optional: Path to CSS stylesheet.", default=None)
    args = parser.parse_args()
    
    convert_md_to_pdf(args.markdown_file, args.css)