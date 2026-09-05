import chromadb
import json

chroma_client = chromadb.PersistentClient(path="./chroma_db_data")

try:
    chroma_client.delete_collection(name="makaut_syllabus")
except Exception:
    pass

collection = chroma_client.get_or_create_collection(name="makaut_syllabus")

allowed_subjects = ["ELECTRIC MACHINE-II", "POWER SYSTEM-I", "CONTROL SYSTEM", "POWER ELECTRONICS"]

with open("data/parsed_ee_sem5.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []
metadatas = []
ids = []

for subject in data:
    subject_name = subject["subject_name"]
    if subject_name not in allowed_subjects:
        continue
    for unit in subject["units"]:
        documents.append(unit["content"])
        metadatas.append({"subject": subject_name, "unit_no": unit["unit_no"], "title": unit["title"]})
        ids.append(f"{subject_name}_{unit['unit_no']}")

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

print(f"Added {collection.count()} documents to collection")