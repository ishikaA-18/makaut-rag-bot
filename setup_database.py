import sqlite3
conn = sqlite3.connect("progress.db")
cursor = conn.cursor()
cursor.execute("""
       CREATE TABLE IF NOT EXISTS progress (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           subject_name TEXT,
           unit_no TEXT,
           unit_title TEXT,
           status TEXT
    )
""")
conn.commit()
conn.close()