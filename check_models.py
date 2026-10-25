import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = client.models.list()
print("Available model IDs for your API key:")
for m in models.data:
    print(f"- {m.id}")