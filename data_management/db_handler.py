import MySQLdb
from datetime import date
from config.settings import log_error

def format_date_for_json(date_obj: date | None) -> str | None:
    """Formats a date object into the string format used in the original JSON."""
    if not date_obj:
        return None
    return date_obj.strftime("%Y-%m-%dT00:00:00")

def _get_db_connection():
    """Helper function to establish a database connection."""
    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'kazi_db',
        'port': 3306
    }
    return MySQLdb.connect(**db_config)

def get_all_firms_summary() -> list[dict] | None:
    """
    Queries the database for a summary of all firms.
    Returns:
        A list of dictionaries, each representing a firm's summary, or None on error.
    """
    cnx = None
    cursor = None
    try:
        cnx = _get_db_connection()
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, firm_name, tagline, approach_summary FROM profiles_firm")
        firms = cursor.fetchall()
        return firms
    except MySQLdb.Error as err:
        log_error(f"Database error fetching firms summary: {err}")
        return None
    finally:
        if cnx:
            cursor.close()
            cnx.close()

def get_all_consultants_summary() -> list[dict] | None:
    """
    Queries the database for a summary of all consultants.
    Returns:
        A list of dictionaries, each representing a consultant's summary, or None on error.
    """
    cnx = None
    cursor = None
    try:
        cnx = _get_db_connection()
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, summary_profile FROM profiles_consultant")
        consultants = cursor.fetchall()
        return consultants
    except MySQLdb.Error as err:
        log_error(f"Database error fetching consultants summary: {err}")
        return None
    finally:
        if cnx:
            cursor.close()
            cnx.close()

def get_consultants_by_firm(firm_id: int) -> list[dict] | None:
    """
    Queries the database for consultants associated with a specific firm.
    Args:
        firm_id: The ID of the firm.
    Returns:
        A list of dictionaries, each representing a consultant's summary, or None on error.
    """
    cnx = None
    cursor = None
    try:
        cnx = _get_db_connection()
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT
                pc.id,
                pc.name,
                pc.email,
                pc.summary_profile
            FROM
                profiles_consultant pc
            JOIN
                profiles_consultant_firms pcf ON pc.id = pcf.consultant_id
            WHERE
                pcf.firm_id = %s
            ORDER BY
                pc.name ASC
        """, (firm_id,))
        consultants = cursor.fetchall()
        return consultants
    except MySQLdb.Error as err:
        log_error(f"Database error fetching consultants by firm {firm_id}: {err}")
        return None
    finally:
        if cnx:
            cursor.close()
            cnx.close()

def get_full_consultant_profile_as_dict(email: str) -> dict | None:
    """
    Queries the MySQL database for a specific consultant and all their related data,
    then returns it as a dictionary mimicking the master_cv.json structure.

    Args:
        email: The email of the consultant to fetch.

    Returns:
        A dictionary containing the full profile, or None if not found.
    """
    cnx = None
    cursor = None
    try:
        cnx = _get_db_connection()
        cursor = cnx.cursor(MySQLdb.cursors.DictCursor)

        # Fetch consultant basic info
        cursor.execute("SELECT id, name, email, phone, linkedin, summary_profile FROM profiles_consultant WHERE email = %s", (email,))
        consultant = cursor.fetchone()
        if not consultant:
            log_error(f"No consultant found with email: {email}")
            return None

        consultant_id = consultant['id']

        # Fetch education
        cursor.execute("SELECT degree, institution, location, start_year, end_year, field_of_study, graduation_status, dissertation_title, dissertation_link FROM profiles_education WHERE consultant_id = %s ORDER BY end_year DESC", (consultant_id,))
        education_list = cursor.fetchall()

        # Fetch certifications
        cursor.execute("SELECT certification_name, issuer, issue_date, expiry_date, description, certification_link FROM profiles_certification WHERE consultant_id = %s ORDER BY issue_date DESC", (consultant_id,))
        certifications_list = cursor.fetchall()

        # Fetch publications
        cursor.execute("SELECT title, authors, year, publisher, link FROM profiles_publication WHERE consultant_id = %s ORDER BY year DESC", (consultant_id,))
        publications_list = cursor.fetchall()

        # Fetch languages
        cursor.execute("SELECT language, level FROM profiles_language WHERE consultant_id = %s", (consultant_id,))
        languages_list = cursor.fetchall()

        # Fetch assignments (roles and projects)
        assignments_list = []
        cursor.execute("""
            SELECT
                pr.title,
                pr.client,
                pr.start_date,
                pr.end_date,
                pr.project_summary,
                cr.role_description,
                cr.tasks,
                pr.sectors,
                pr.methodologies
            FROM
                profiles_consultantrole cr
            JOIN
                profiles_project pr ON cr.project_id = pr.id
            WHERE
                cr.consultant_id = %s
            ORDER BY
                pr.start_date DESC
        """, (consultant_id,))
        roles_projects = cursor.fetchall()

        for rp in roles_projects:
            start_str = rp['start_date'].strftime('%b %Y') if rp['start_date'] else 'N/A'
            end_str = rp['end_date'].strftime('%b %Y') if rp['end_date'] else 'Present'
            
            # Handle JSON fields that might be strings from DB
            sectors = eval(rp['sectors']) if isinstance(rp['sectors'], str) else rp['sectors']
            methodologies = eval(rp['methodologies']) if isinstance(rp['methodologies'], str) else rp['methodologies']

            assignments_list.append({
                "title": rp['title'],
                "organization": rp['client'],
                "location": None, # Not directly available in current schema, can be added to project if needed
                "date_range": f"{start_str} – {end_str}",
                "start_date": format_date_for_json(rp['start_date']),
                "description": rp['role_description'],
                "project_summary": rp['project_summary'],
                "role_summary": rp['role_description'],
                "tasks": rp['tasks'],
                "sectors": sectors or [],
                "methodologies": methodologies or []
            })

        profile_dict = {
            "name": consultant['name'],
            "email": consultant['email'],
            "phone": consultant['phone'],
            "linkedin": consultant['linkedin'],
            "summary_profile": consultant['summary_profile'],
            "education": [{k: format_date_for_json(v) if isinstance(v, date) else v for k, v in edu.items()} for edu in education_list],
            "certifications": [{k: format_date_for_json(v) if isinstance(v, date) else v for k, v in cert.items()} for cert in certifications_list],
            "publications": publications_list,
            "languages": languages_list,
            "assignments": assignments_list,
        }

        return profile_dict

    except MySQLdb.Error as err:
        log_error(f"Database error: {err}")
        return None
    finally:
        if 'cnx' in locals():
            cursor.close()
            cnx.close()
