import httpx
import base64
import os
from config import HF_API_KEY

# Free model from Hugging Face
#HF_MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HF_MODEL_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"

async def generate_image(query: str) -> str:
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    payload = {
        "inputs": query
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(HF_MODEL_URL, headers=headers, json=payload)

    if response.status_code == 200:
        # Image bytes ko base64 mein convert karo
        image_bytes = response.content
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        
        # Save kar lo locally bhi
        filename = f"generated_{query[:20].replace(' ', '_')}.png"
        filepath = f"static/generated/{filename}"
        os.makedirs("static/generated", exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return f"Image generated successfully!\nFile saved: {filepath}\nBase64 preview available."
    
    elif response.status_code == 503:
        return "Model load ho raha hai, 20 seconds baad dobara try karo!"
    
    else:
        return f"Image generation failed: {response.status_code} - {response.text}"