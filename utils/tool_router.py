# Simple tool router - decides which tool to use based on user query
import re

def route_tool(query: str) -> str:
    query_lower = query.lower()

    # Task agent - when multiple actions needed
    if any(word in query_lower for word in ["and also", "both", "as well as", "additionally"]):
        return "task_agent"

    # Image generation
    if any(word in query_lower for word in ["generate image", "create image", "draw", "picture of", "image of", "make an image"]):
        return "image_generator"

    # Text generation  
    if any(word in query_lower for word in ["write", "blog", "essay", "summarize", "summary", "explain", "article", "draft", "create a story"]):
        return "text_generator"

    # Default - chat handler
    return "chat_handler"

