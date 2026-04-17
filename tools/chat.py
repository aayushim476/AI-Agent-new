from groq import Groq
from config import GROQ_API_KEY

async def handle_chat(query: str, history: list = []) -> str:
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Remember everything the user tells you in this conversation and use it when answering."}
    ]

    # Pichli history add karo
    messages.extend(history)

    # Naya message add karo
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=500
    )
    return response.choices[0].message.content