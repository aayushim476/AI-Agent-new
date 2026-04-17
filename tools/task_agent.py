from tools.text_gen import generate_text
from tools.image_gen import generate_image

async def run_task_agent(query: str) -> str:
    """Handle multi-step tasks that require multiple tools"""
    results = []
    query_lower = query.lower()

    # Step 1: Check if text generation is needed
    needs_text = any(word in query_lower for word in ["write", "blog", "essay", "article", "story", "text"])
    # Step 2: Check if image generation is needed
    needs_image = any(word in query_lower for word in ["image", "picture", "draw", "generate image"])

    if needs_text:
        text_prompt = f"Write content about: {query}"
        text_result = await generate_text(text_prompt)
        results.append(f"--- TEXT GENERATED ---\n{text_result}")

    if needs_image:
        image_prompt = query.replace("write", "").replace("blog", "").strip()
        image_result = await generate_image(image_prompt)
        results.append(f"--- IMAGE GENERATED ---\n{image_result}")

    if not results:
        results.append("Task agent: No specific tools matched. Please clarify your request.")

    return "\n\n".join(results)
