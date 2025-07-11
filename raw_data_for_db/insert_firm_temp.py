
import sqlite3
import json

db_path = "G:\My Drive\James\Kazi\kazi\data_management\kazi.db"

conn = None
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    firm_name = "One South LLC"
    firm_description = """
One South is an international development consulting firm that supports organizations to understand and deliver social change. Since our founding in 2014, we have evaluated programs representing over $140M in donor funding across 40+ countries in the areas of health, education, human rights, and economic empowerment. 
We have supported projects funded by Global Affairs Canada, the US Department of State, the UK Foreign and Commonwealth Office, the European Commission, Irish AID, The World Bank, UNESCO, and several foundations. We have worked in Africa, Asia, Latin America, the Middle East, Eastern Europe and Central Asia, and the Caribbean. 
Our team is composed of sector specialists with cross-cutting expertise in monitoring, evaluation & learning, gender, and social inclusion. All of our team members have deep roots in the global south, with experience living and working in developing contexts.    

We believe enhancing in-country research capacity supports the long term sustainability of development outcomes and the sustainability of evidence-informed decision making. We therefore work closely with in-country partners, bringing together local and global experts to deliver contextualized planning, monitoring, and evaluation advice. We seek to empower local actors to lead development initiatives within their communities, recognizing the importance of development aid localization, co-creation, and partnership. This means we place particular emphasis on the use of participatory methods, on co-designing systems, and on growing shared ownership and fostering buy-in amongst key stakeholders.
"""
    firm_capabilities = json.dumps([
        "Monitoring, Evaluation & Learning (MEL)",
        "Gender and Social Inclusion (GESI)",
        "Health Programs Evaluation",
        "Education Programs Evaluation",
        "Human Rights Programs Evaluation",
        "Economic Empowerment Programs Evaluation",
        "In-country Research Capacity Building",
        "Participatory Methods",
        "Co-designing Systems"
    ])
    firm_values = json.dumps([
        "Social change is experimental, incremental, and driven by a shared experience",
        "Using information to understand and deliver social change",
        "Enhancing in-country research capacity supports long-term sustainability of development outcomes and evidence-informed decision making",
        "Empowering local actors to lead development initiatives",
        "Development aid localization, co-creation, and partnership",
        "Participatory methods",
        "Co-designing systems",
        "Growing shared ownership and fostering buy-in amongst key stakeholders"
    ])
    address = None # Not provided in the text
    email = "management@one-south.org"

    cursor.execute("""
        INSERT INTO firms (firm_name, firm_description, firm_capabilities, firm_values, address, email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (firm_name, firm_description, firm_capabilities, firm_values, address, email))
    
    conn.commit()
    print(f"Firm '{firm_name}' inserted successfully.")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
    if conn:
        conn.rollback()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if conn:
        conn.close()
