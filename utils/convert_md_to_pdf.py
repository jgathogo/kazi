import os
from weasyprint import HTML
import markdown

def convert_md_to_pdf(md_filepath: str, css_filepath: str | None = None) -> str | None:
    """
    Converts a Markdown file to a PDF file.

    Args:
        md_filepath: The absolute or relative path to the input Markdown file.
        css_filepath: Optional. The absolute or relative path to the CSS stylesheet.
                      If None, the script will look for 'resume_markdown_pdf_style.css'
                      in the same directory as the Markdown file.

    Returns:
        The full path to the generated PDF file, or None if an error occurs.
    """
    script_directory = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.abspath(md_filepath)

    # Determine CSS path
    stylesheets_to_load = []
    if css_filepath:
        css_path = os.path.abspath(css_filepath)
    else:
        css_path = os.path.join(script_directory, "resume_markdown_pdf_style.css")
    if os.path.exists(css_path):
        stylesheets_to_load = [css_path]
        print(f"INFO: Found CSS stylesheet at: {css_path}")
    else:
        print(f"WARNING: CSS file not found at: {css_path}. PDF will be generated without this stylesheet.")

    if not os.path.exists(md_path):
        print(f"ERROR: Markdown file not found at: {md_path}")
        return None

    pdf_file_name = os.path.splitext(os.path.basename(md_path))[0] + ".pdf"
    pdf_path = os.path.join(os.path.dirname(md_path), pdf_file_name)

    print(f"INFO: Reading Markdown from: {md_path}")
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
    <title>Converted PDF</title>
    {"<link rel='stylesheet' href='" + css_path + "'>" if os.path.exists(css_path) else ""}
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
    import argparse
    parser = argparse.ArgumentParser(description="Convert a Markdown file to PDF.")
    parser.add_argument("markdown_file", type=str, help="Path to the Markdown file.")
    parser.add_argument("--css", type=str, help="Optional: Path to CSS stylesheet.", default=None)
    args = parser.parse_args()
    convert_md_to_pdf(args.markdown_file, args.css) 