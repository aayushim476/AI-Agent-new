from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskRequest(BaseModel):
    query: str
    session_id: str
    pdf_text: Optional[str] = None

class TaskResponse(BaseModel):
    id: Optional[str] = None
    query: str
    tool_used: str
    result: str
    username: str
    created_at: Optional[datetime] = None