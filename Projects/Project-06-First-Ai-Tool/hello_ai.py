import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load variables from .env
load_dotenv()

# 2. Grab your key
api_key = os.getenv("OPENROUTER_API_KEY")

# 3. Check if the key was actually loaded
if not api_key:
    raise ValueError("ERROR: Could not find OPENROUTER_API_KEY. Check your .env file name and location!")

# 4. Initialize client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# 5. Ask question
user_question = input("Ask the AI anything: ")

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "user", "content": user_question}
    ],
)

ai_reply = response.choices[0].message.content
print("\nAI Response:")
print(ai_reply)