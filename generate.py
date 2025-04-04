import groq
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

client = groq.Client(api_key=groq_api_key)

def generate_response(prompt_text):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt_text}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API Error: {e}"
