import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
model_name="gemini-flash-latest"
client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(model=model_name, contents="Hello, are you working?")
#for m in client.models.list():
    #print(m.name)
print(response.text)
