from groq import Groq
from config import GROQ_API_KEY

async def generate_text(query: str, history: list = []) -> str:
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Give direct answers only. Do not show your thinking process, reasoning steps, or internal thoughts. Just give the final answer directly."}
    ]

    messages.extend(history)
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        max_tokens=800
    )
    return response.choices[0].message.content
