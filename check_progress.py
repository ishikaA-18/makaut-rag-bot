import sqlite3
conn = sqlite3.connect("progress.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM progress WHERE subject_name = 'POWER ELECTRONICS'")
for row in cursor.fetchall():
    print(row)
conn.close()