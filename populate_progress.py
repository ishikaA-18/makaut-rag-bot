import sqlite3
import json
with open("data/parsed_ee_sem5.json", "r", encoding="utf-8") as f:
    data = json.load(f)
conn = sqlite3.connect("progress.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM progress")
allowed_subjects = ["ELECTRIC MACHINE-II", "POWER SYSTEM-I", "CONTROL SYSTEM", "POWER ELECTRONICS"]
for subject in data:
    subject_name = subject["subject_name"]
    if subject_name not in allowed_subjects:
           continue
    for unit in subject["units"]:
        cursor.execute(
               "INSERT INTO progress (subject_name, unit_no, unit_title, status) VALUES (?, ?, ?, ?)",
               (subject_name, unit["unit_no"], unit["title"], "pending")
           )
conn.commit()
conn.close()
print("Progress table populated!")