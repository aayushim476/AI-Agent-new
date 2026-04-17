from groq import Groq
from config import GROQ_API_KEY

async def generate_text(query: str, history: list = []) -> str:
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {"role": "system", "content": "You are a helpful writing assistant. Remember everything the user tells you."}
    ]

    messages.extend(history)
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=800
    )
    return response.choices[0].message.content