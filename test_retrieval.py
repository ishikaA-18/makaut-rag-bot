import chromadb
import pprint
chroma_client = chromadb.PersistentClient(path="./chroma_db_data")
collection = chroma_client.get_or_create_collection(name="makaut_syllabus")
query_text = "How do I make tea?"
results = collection.query(
    query_texts=[query_text],
    n_results=2  
)
print("--- Query Results ---")
pprint.pprint(results)