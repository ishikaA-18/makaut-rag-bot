import chromadb
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
chroma_client = chromadb.PersistentClient(path="./chroma_db_data")
collection = chroma_client.get_or_create_collection(name="makaut_syllabus")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
model_name="gemini-flash-latest"
client = genai.Client(api_key=GEMINI_API_KEY)
user_question = "Power Electronics mein inverters ke baare mein kya hai?"
results = collection.query(query_texts=[user_question], n_results=2)
print("--- DEBUG: Retrieved chunks ---")
for i, doc in enumerate(results['documents'][0]):
    print(f"\nChunk {i} (metadata: {results['metadatas'][0][i]}):")
    print(doc)
print("--- END DEBUG ---\n")
retrieved_chunks = results['documents'][0]
context_string = "\n\n".join(retrieved_chunks)
prompt = f"""You are a helpful study assistant for MAKAUT Electrical Engineering students.
Answer the student's question using ONLY the context below. If the answer isn't in the context, say you don't have that information in the syllabus.

Context:
{context_string}

Question: {user_question}
"""
response = client.models.generate_content(model=model_name, contents=prompt)
print(response.text)