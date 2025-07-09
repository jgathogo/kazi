
import sqlite3

db_path = "G:\My Drive\James\Kazi\kazi\data_management\kazi.db"

conn = None
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT firm_id, firm_name, email FROM firms;")
    firms = cursor.fetchall()

    if firms:
        print("Firms in the database:")
        for firm in firms:
            print(f"ID: {firm[0]}, Name: {firm[1]}, Email: {firm[2]}")
    else:
        print("No firms found in the database.")

except sqlite3.Error as e:
    print(f"SQLite error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if conn:
        conn.close()
