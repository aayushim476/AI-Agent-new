from groq import Groq
from config import GROQ_API_KEY

async def generate_text(query: str, history: list = []) -> str:
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Give direct, concise answers only. Never show thinking process, reasoning steps, or internal analysis. Just answer directly and naturally."}
    ]

    messages.extend(history)
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",,
        messages=messages,
        max_tokens=800
    )
    return response.choices[0].message.content
