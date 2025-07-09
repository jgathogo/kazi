
import sqlite3
import os
import sys

db_path = "G:\My Drive\James\Kazi\kazi\data_management\kazi.db"
db_dir = os.path.dirname(db_path)

try:
    os.makedirs(db_dir, exist_ok=True)
    print(f"Directory '{db_dir}' ensured to exist.", file=sys.stderr)
except Exception as e:
    print(f"Error ensuring directory '{db_dir}': {e}", file=sys.stderr)
    sys.exit(1)

conn = None
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"Successfully connected to database at '{db_path}'.", file=sys.stderr)

    # Table for Firms
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS firms (
        firm_id INTEGER PRIMARY KEY AUTOINCREMENT,
        firm_name TEXT NOT NULL UNIQUE,
        firm_description TEXT,
        firm_capabilities TEXT,
        firm_values TEXT,
        address TEXT,
        email TEXT
    );
    """)
    print("Table 'firms' created or already exists.", file=sys.stderr)

    # Table for Individual Consultants
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultants (
        consultant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        firm_id INTEGER,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        linkedin TEXT,
        bio TEXT,
        professional_summary TEXT,
        FOREIGN KEY (firm_id) REFERENCES firms(firm_id)
    );
    """)
    print("Table 'consultants' created or already exists.", file=sys.stderr)

    # Table for Consultant's Assignments/Experience
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        consultant_id INTEGER NOT NULL,
        firm_id INTEGER,
        title TEXT NOT NULL,
        organization TEXT,
        location TEXT,
        start_date DATE,
        end_date DATE,
        date_range TEXT,
        description TEXT,
        project_summary TEXT,
        role_summary TEXT,
        tasks TEXT,
        sectors TEXT,
        methodologies TEXT,
        achievements TEXT,
        FOREIGN KEY (consultant_id) REFERENCES consultants(consultant_id),
        FOREIGN KEY (firm_id) REFERENCES firms(firm_id)
    );
    """)
    print("Table 'assignments' created or already exists.", file=sys.stderr)

    # Tables for individual consultant's static data
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS education (
        education_id INTEGER PRIMARY KEY AUTOINCREMENT,
        consultant_id INTEGER NOT NULL,
        degree TEXT,
        institution TEXT,
        location TEXT,
        start_year DATE,
        end_year DATE,
        field_of_study TEXT,
        graduation_status TEXT,
        dissertation_link TEXT,
        disseration_title TEXT,
        FOREIGN KEY (consultant_id) REFERENCES consultants(consultant_id)
    );
    """)
    print("Table 'education' created or already exists.", file=sys.stderr)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certifications (
        certification_id INTEGER PRIMARY KEY AUTOINCREMENT,
        consultant_id INTEGER NOT NULL,
        certification_name TEXT,
        issuer TEXT,
        issue_date DATE,
        expiry_date DATE,
        description TEXT,
        certification_link TEXT,
        FOREIGN KEY (consultant_id) REFERENCES consultants(consultant_id)
    );
    """)
    print("Table 'certifications' created or already exists.", file=sys.stderr)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS publications (
        publication_id INTEGER PRIMARY KEY AUTOINCREMENT,
        consultant_id INTEGER NOT NULL,
        title TEXT,
        authors TEXT,
        year INTEGER,
        publisher TEXT,
        link TEXT,
        FOREIGN KEY (consultant_id) REFERENCES consultants(consultant_id)
    );
    """)
    print("Table 'publications' created or already exists.", file=sys.stderr)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS languages (
        language_id INTEGER PRIMARY KEY AUTOINCREMENT,
        consultant_id INTEGER NOT NULL,
        language TEXT,
        level TEXT,
        FOREIGN KEY (consultant_id) REFERENCES consultants(consultant_id)
    );
    """)
    print("Table 'languages' created or already exists.", file=sys.stderr)

    # Optional: Skills and Consultant-Skills tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT NOT NULL UNIQUE,
        category TEXT
    );
    """)
    print("Table 'skills' created or already exists.", file=sys.stderr)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultant_skills (
        consultant_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        consultant_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        proficiency_level TEXT,
        FOREIGN KEY (consultant_id) REFERENCES consultants(consultant_id),
        FOREIGN KEY (skill_id) REFERENCES skills(skill_id),
        UNIQUE (consultant_id, skill_id)
    );
    """)
    print("Table 'consultant_skills' created or already exists.", file=sys.stderr)

    conn.commit()
    print("All tables created/ensured and changes committed.", file=sys.stderr)

except sqlite3.Error as e:
    print(f"SQLite error: {e}", file=sys.stderr)
    if conn:
        conn.rollback()
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)
finally:
    if conn:
        conn.close()
        print("Database connection closed.", file=sys.stderr)
