import sqlite3
conn = sqlite3.connect("progress.db")
cursor = conn.cursor()

subject_to_update = "POWER ELECTRONICS"
unit_to_update = "5"
new_status = "completed"

cursor.execute(
    "UPDATE progress SET status = ? WHERE subject_name = ? AND unit_no = ?",
    (new_status, subject_to_update, unit_to_update)
)

print(f"Rows updated: {cursor.rowcount}")
conn.commit()
conn.close()