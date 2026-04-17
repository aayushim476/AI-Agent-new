from fastapi import APIRouter, Depends, HTTPException
from models.task import TaskRequest, TaskResponse
from database import tasks_collection, sessions_collection
from utils.auth_utils import get_current_user
from utils.tool_router import route_tool
from tools.text_gen import generate_text
from tools.image_gen import generate_image
from tools.chat import handle_chat
from tools.task_agent import run_task_agent
from datetime import datetime
from groq import Groq
from config import GROQ_API_KEY
import uuid

router = APIRouter(prefix="/agent", tags=["AI Agent"])

@router.post("/session/new")
async def new_session(current_user: str = Depends(get_current_user)):
    session_id = str(uuid.uuid4())
    await sessions_collection.insert_one({
        "session_id": session_id,
        "username": current_user,
        "title": "New Chat",
        "created_at": datetime.utcnow(),
        "is_deleted": False
    })
    return {"session_id": session_id}


@router.get("/sessions")
async def get_sessions(current_user: str = Depends(get_current_user)):
    sessions = []
    cursor = sessions_collection.find(
        {"username": current_user}
    ).sort("created_at", -1).limit(20)
    async for s in cursor:
        s["_id"] = str(s["_id"])
        sessions.append(s)
    return {"sessions": sessions}

@router.post("/run", response_model=TaskResponse)
async def run_agent(
    request: TaskRequest,
    current_user: str = Depends(get_current_user)
):
    query = request.query.strip()
    session_id = request.session_id
    pdf_text = request.pdf_text  # PDF text agar hai toh

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Session exist nahi karta toh bana do
    session = await sessions_collection.find_one({"session_id": session_id})
    if not session:
        await sessions_collection.insert_one({
            "session_id": session_id,
            "username": current_user,
            "title": query[:40],
            "created_at": datetime.utcnow()
        })
    else:
        if session.get("title") == "New Chat":
            await sessions_collection.update_one(
                {"session_id": session_id},
                {"$set": {"title": query[:40]}}
            )

    # Session ki history lo
    history = []
    cursor = tasks_collection.find(
        {"username": current_user, "session_id": session_id}
    ).sort("created_at", 1)
    async for task in cursor:
        history.append({"role": "user", "content": task["query"]})
        history.append({"role": "assistant", "content": task["result"]})

    # Agar PDF text hai toh directly Groq se answer lo
    if pdf_text:
        result = await handle_pdf_query(query, pdf_text, history)
        tool = "pdf_agent"
    else:
        tool = route_tool(query)
        if tool == "text_generator":
            result = await generate_text(query, history=history)
        elif tool == "image_generator":
            result = await generate_image(query)
        elif tool == "task_agent":
            result = await run_task_agent(query)
        else:
            result = await handle_chat(query, history=history)

    # MongoDB mein save karo
    task_doc = {
        "query": query,
        "tool_used": tool,
        "result": result,
        "username": current_user,
        "session_id": session_id,
        "created_at": datetime.utcnow()
    }
    inserted = await tasks_collection.insert_one(task_doc)

    return TaskResponse(
        id=str(inserted.inserted_id),
        query=query,
        tool_used=tool,
        result=result,
        username=current_user,
        created_at=task_doc["created_at"]
    )

async def handle_pdf_query(query: str, pdf_text: str, history: list = []) -> str:
    """PDF text + user query Groq ko do"""
    try:
        client = Groq(api_key=GROQ_API_KEY)

        # PDF text too lamba ho toh trim karo (Groq context limit)
        max_chars = 12000
        if len(pdf_text) > max_chars:
            pdf_text = pdf_text[:max_chars] + "\n\n[...PDF truncated...]"

        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful assistant. The user has uploaded a PDF document.
Here is the PDF content:

---
{pdf_text}
---

Answer the user's questions based on this PDF content and your own knowledge."""
            }
        ]

        messages.extend(history)
        messages.append({"role": "user", "content": query})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"PDF query error: {str(e)}"

@router.get("/history")
async def get_history(
    session_id: str,
    current_user: str = Depends(get_current_user)
):
    tasks = []
    cursor = tasks_collection.find(
        {"username": current_user, "session_id": session_id}
    ).sort("created_at", 1)
    async for task in cursor:
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return {"tasks": tasks}

@router.delete("/session/{session_id}")
async def delete_session(
    session_id: str,
    current_user: str = Depends(get_current_user)
):
    await sessions_collection.update_one(
        {"session_id": session_id},
        {"$set": {"is_deleted": True}}
    )
    return {"message": "Session deleted"}