# File: kazi/utils/static_content_builder.py
# This is based on your cv_static_builder.py
# Ensure you have 'python-dateutil' installed (pip install python-dateutil)

import os
from dateutil import parser as date_parser
import json # Not strictly needed here if functions take parsed data, but good for context
from config import settings # For logging if needed

def format_date_for_cv(date_str, desired_format="%Y"):
    if not date_str:
        return ""
    try:
        # Handle cases where year might be float like 2025.0 from JSON
        if isinstance(date_str, float):
            date_str = str(int(date_str))
        elif isinstance(date_str, int):
             date_str = str(date_str)

        # Try parsing as ISO date first if it contains T or Z
        if 'T' in date_str or 'Z' in date_str or '+' in date_str.split('T')[-1]:
            dt_obj = date_parser.isoparse(date_str)
        else: # Attempt to parse other common date/year formats
            dt_obj = date_parser.parse(date_str)
        return dt_obj.strftime(desired_format)
    except (ValueError, TypeError, AttributeError) as e:
        # Fallback for simple year strings or already formatted dates
        s_date_str = str(date_str)
        if len(s_date_str) >= 4 and s_date_str[:4].isdigit():
            return s_date_str[:4] # Return first 4 digits if it looks like a year
        # settings.log_info(f"Could not parse date '{date_str}' with format '{desired_format}', returning as is. Error: {e}")
        return s_date_str # Fallback to returning the string as is

def build_personal_md(cv_data: dict) -> str:
    name = cv_data.get("name", "Your Name")
    phone = cv_data.get("phone", "")
    email = cv_data.get("email", "")
    linkedin_url = cv_data.get("linkedin", "")
    
    contact_parts = []
    if phone:
        # Basic cleaning for tel link, you might want more sophisticated parsing
        tel_phone = ''.join(filter(lambda char: char.isdigit() or char == '+', phone))
        if phone.startswith('+') and not tel_phone.startswith('+'): # Ensure '+' is kept if present
            tel_phone = '+' + tel_phone
        contact_parts.append(f"[{phone}](tel:{tel_phone})")
    if email:
        contact_parts.append(f"[{email}](mailto:{email})")
    if linkedin_url:
        # Assuming you want the plain text version as per your earlier example
        # For a clickable link: contact_parts.append(f"[LinkedIn]({linkedin_url})")
        # linkedin_display = linkedin_url.replace('https://','').replace('http://','')
        contact_parts.append(f"[LinkedIn]({linkedin_url})") # Making it a clickable link
        # If you want the URL to show as text AND be clickable, revert to:
        # linkedin_display = linkedin_url.replace('https://','').replace('http://','')
        # contact_parts.append(f"LinkedIn: [{linkedin_display}]({linkedin_url})")

    contact_line = " | ".join(contact_parts)
    # Using H1 for name as per your cv_static_builder.py example output
    return f"# {name}\n{contact_line}\n"


def build_education_md(education_list: list | None) -> str:
    if not education_list:
        return "## Education\n*No education data provided.*"
    md_parts = ["## Education", ""]

    def get_education_sort_key(edu_item):
        # Prioritize end_year, then start_year for sorting
        sort_date_str = edu_item.get("end_year") or edu_item.get("start_year")
        if sort_date_str:
            try:
                # Handle float years like 2014.0
                if isinstance(sort_date_str, float): sort_date_str = str(int(sort_date_str))
                return date_parser.parse(str(sort_date_str))
            except (ValueError, TypeError):
                # Fallback for unparseable dates, sort them to the beginning or end
                return date_parser.parse("1900-01-01T00:00:00Z") 
        return date_parser.parse("1900-01-01T00:00:00Z") # Default for items with no date

    # Sort education entries, most recent first
    sorted_education = sorted(education_list, key=get_education_sort_key, reverse=True)

    for edu in sorted_education:
        degree = edu.get("degree", "N/A")
        institution = edu.get("institution", "N/A")
        location = edu.get("location", "") # Location from JSON
        
        start_year_str = format_date_for_cv(edu.get("start_year"), desired_format="%Y")
        end_year_str = format_date_for_cv(edu.get("end_year"), desired_format="%Y")

        date_range = ""
        if edu.get("graduation_status", "").lower() == "graduated" and end_year_str:
            date_range = f"(Graduated {end_year_str})"
        elif start_year_str and end_year_str and start_year_str != end_year_str:
            date_range = f"({start_year_str}–{end_year_str})"
        elif end_year_str: # Only end year provided
            date_range = f"({end_year_str})"
        elif start_year_str: # Only start year, assume ongoing or completion year not specified
            date_range = f"({start_year_str}–Present)" # Or just f"({start_year_str})"

        institution_display = institution
        if location and location.lower() not in institution.lower():
            institution_display += f", {location}"
        
        md_parts.append(f"- **{degree}** | {institution_display} {date_range}")

        dissertation_title = edu.get("disseration_title") # Field name from your example
        if dissertation_title:
            diss_link_raw = edu.get("dissertation_link")
            diss_link_cleaned = None
            if diss_link_raw and isinstance(diss_link_raw, str):
                # Clean common wrapping characters like '#' if present
                diss_link_cleaned = diss_link_raw.strip().strip('#')
            
            if diss_link_cleaned:
                md_parts.append(f"    - *Thesis:* [{dissertation_title}]({diss_link_cleaned})")
            else:
                md_parts.append(f"    - *Thesis:* {dissertation_title}")
    return "\n".join(md_parts)


def build_certifications_md(cert_list: list | None, max_certs=5) -> str:
    if not cert_list:
        return "## Certifications (Selected)\n*No certifications listed.*"
    md_parts = ["## Certifications (Selected)", ""]

    def get_cert_sort_key(cert_item):
        issue_date = cert_item.get("issue_date") # Expects ISO date string e.g. "2020-05-01T00:00:00Z"
        if issue_date:
            try: return date_parser.isoparse(issue_date)
            except (ValueError, TypeError): return date_parser.parse("1900-01-01T00:00:00Z")
        return date_parser.parse("1900-01-01T00:00:00Z")

    sorted_certs = sorted(cert_list, key=get_cert_sort_key, reverse=True)
    
    for cert in sorted_certs[:max_certs]:
        name = cert.get("certification_name", "N/A")
        issuer = cert.get("issuer", "N/A")
        date_formatted = format_date_for_cv(cert.get("issue_date"), desired_format="%Y") # Just year
        link = cert.get("certification_linke") # Field name from your example 'certification_linke'
        
        cert_text = name
        if link and isinstance(link, str) and link.strip():
            cert_text = f"[{name}]({link.strip()})"
        
        md_parts.append(f"* {cert_text} | {issuer} ({date_formatted})")
            
    return "\n".join(md_parts)


def build_publications_md(pub_list: list | None, max_pubs=5) -> str:
    if not pub_list:
        return "## Publications (Selected)\n*No publications listed.*"
    md_parts = ["## Publications (Selected)", ""]
    md_parts.append("_Click on each title to access the document – most are hosted on client websites_")
    # md_parts.append("") # Adding extra line for spacing

    def get_pub_sort_key(pub_item):
        year_val = pub_item.get("year") # e.g., 2025 or "2025" or 2025.0
        if year_val:
            try: return int(float(str(year_val))) # Convert to float then int to handle "2025.0"
            except ValueError: return 0
        return 0

    sorted_pubs = sorted(pub_list, key=get_pub_sort_key, reverse=True)

    for pub in sorted_pubs[:max_pubs]:
        title = pub.get("title", "N/A")
        link_url = pub.get("link")
        authors = pub.get("authors", "")
        publisher = pub.get("publisher", "")
        year_val = pub.get("year")
        year_str = format_date_for_cv(year_val, desired_format="%Y")

        pub_line = "- "
        if authors:
            pub_line += f"{authors} ({year_str}). "
        elif year_str:
            pub_line += f"({year_str}). "

        title_md = f"*{title}*"
        if link_url and isinstance(link_url, str) and link_url.strip():
            title_md = f"*[{title}]({link_url.strip()})*"
        
        pub_line += title_md
        
        if publisher:
            pub_line += f", _{publisher}_"
            
        md_parts.append(pub_line)
    return "\n".join(md_parts)


def build_languages_md(languages_data: list | None) -> str:
    if languages_data and isinstance(languages_data, list):
        if not languages_data:
            return "## Languages\n* English (Native)\n* Kiswahili (Fluent)"
        
        md_parts = ["## Languages"]
        # Create a single line with all languages formatted nicely
        lang_parts = [
            f"*{entry['language']}* ({entry['level']})"
            for entry in languages_data
            if 'language' in entry and 'level' in entry
        ]
        md_parts.append(" | ".join(lang_parts))
        return "\n".join(md_parts)
    else:
        return "## Languages\n* English (Fluent)\n* Kiswahili (First langauge)"


# --- Test Script Section (Optional - for direct testing of this file) ---
if __name__ == "__main__":
    # This part will only run if you execute static_content_builder.py directly
    # For it to work, it needs access to settings.py for PROJECT_ROOT or a hardcoded path
    # For simplicity, we'll assume master_cv.json is in a known relative path for testing
    
    # Simplified settings for direct testing
    class TestSettings:
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # kazi/
        CV_DATA_DIR = os.path.join(PROJECT_ROOT, "cv_data")
        MASTER_CV_FILENAME = "master_cv.json"
        
        @staticmethod
        def log_info(message): print(f"INFO: {message}")
        @staticmethod
        def log_error(message): print(f"ERROR: {message}")

    settings = TestSettings() # Override the imported settings for local test

    master_cv_path_test = os.path.join(settings.CV_DATA_DIR, settings.MASTER_CV_FILENAME)
    
    cv_data_test = None
    try:
        with open(master_cv_path_test, 'r', encoding='utf-8') as f:
            cv_data_test = json.load(f)
        settings.log_info(f"Successfully read test CV data from '{master_cv_path_test}'\n")
    except FileNotFoundError:
        settings.log_error(f"Error: Test CV data file not found at '{master_cv_path_test}'.")
    except json.JSONDecodeError:
        settings.log_error(f"Error: Could not decode JSON from '{master_cv_path_test}'.")

    if cv_data_test:
        personal_md = build_personal_md(cv_data_test)
        education_md = build_education_md(cv_data_test.get("education"))
        certifications_md = build_certifications_md(cv_data_test.get("certifications"))
        publications_md = build_publications_md(cv_data_test.get("publications"))
        languages_md = build_languages_md(cv_data_test.get("languages"))

        full_static_cv_md = (
            f"{personal_md}\n\n"
            f"{education_md}\n\n"
            f"{certifications_md}\n\n"
            f"{publications_md}\n\n"
            f"{languages_md}"
        )

        output_test_file = os.path.join(settings.PROJECT_ROOT, "output", "test_static_cv_parts.md")
        # Ensure output directory exists for test
        os.makedirs(os.path.join(settings.PROJECT_ROOT, "output"), exist_ok=True)

        try:
            with open(output_test_file, 'w', encoding='utf-8') as f:
                f.write(full_static_cv_md)
            settings.log_info(f"Static CV sections test output saved to: '{output_test_file}'")
            # print("\n--- Content of test_static_cv_output.md ---")
            # print(full_static_cv_md)
            # print("--- End of Content ---")
        except Exception as e:
            settings.log_error(f"Error writing test output to {output_test_file}: {e}")
