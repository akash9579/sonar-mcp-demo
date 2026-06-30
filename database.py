import sqlite3

def execute_query(raw_query: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # VULNERABLE: raw string interpolation, no sanitization
    cursor.execute(f"SELECT * FROM users WHERE name = '{raw_query}'")
    return cursor.fetchall()