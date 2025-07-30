import os
import argparse
from weasyprint import HTML
import markdown

# Import the formatter from the adjacent utility script
try:
    from .markdown_formatter import format_markdown_file
except ImportError:
    from markdown_formatter import format_markdown_file

def convert_cover_letter_md_to_pdf(md_filepath: str, css_filepath: str | None = None) -> str | None:
    """
    Converts a Markdown cover letter file to a PDF file after cleaning and formatting.
    Uses a cover letter-specific CSS by default.

    Args:
        md_filepath: Path to the input Markdown file.
        css_filepath: Optional path to a CSS stylesheet. Defaults to 'cover_letter_pdf_style.css'.

    Returns:
        The full path to the generated PDF file, or None if an error occurs.
    """
    script_directory = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.abspath(md_filepath)

    if not os.path.exists(md_path):
        print(f"ERROR: Markdown file not found at: {md_path}")
        return None

    print(f"INFO: Formatting Markdown file: {md_path}")
    format_markdown_file(md_path)

    # Use the provided CSS file, or default to the cover letter CSS
    css_path_to_use = css_filepath if css_filepath else os.path.join(script_directory, "cover_letter_pdf_style.css")
    stylesheets_to_load = []
    if os.path.exists(css_path_to_use):
        stylesheets_to_load.append(css_path_to_use)
        print(f"INFO: Using CSS stylesheet at: {css_path_to_use}")
    else:
        print(f"WARNING: CSS file not found at: {css_path_to_use}. PDF will have basic styling.")

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
    html_body = markdown.markdown(md_text, extensions=['fenced_code', 'tables', 'toc'])

    html_full = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset=\"utf-8\">
    <title>Cover Letter PDF</title>
</head>
<body>
    {html_body}
</body>
</html>"""

    print(f"INFO: Converting HTML to PDF, saving to: {pdf_path}")
    try:
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
    parser = argparse.ArgumentParser(description="Convert a Markdown cover letter to PDF after auto-formatting.")
    parser.add_argument("markdown_file", type=str, help="Path to the Markdown cover letter file.")
    parser.add_argument("--css", type=str, help="Optional: Path to CSS stylesheet.", default=None)
    args = parser.parse_args()
    convert_cover_letter_md_to_pdf(args.markdown_file, args.css) 