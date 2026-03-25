# test_groq.py

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"✅ API Key: {api_key[:15]}...")

client = Groq(api_key=api_key)

print("🤖 Sending test to Groq...")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Say hello in one sentence."}
    ]
)

print("✅ Response:", response.choices[0].message.content)