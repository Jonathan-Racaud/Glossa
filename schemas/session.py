from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int
    flashcard_ids: List[int]
    status: str = "active"

class SessionUpdate(BaseModel):
    status: Optional[str] = None
    completed_at: Optional[datetime] = None
    results: Optional[List[dict]] = None

class SessionResponse(BaseModel):
    id: int
    user_id: int
    flashcard_ids: List[int]
    status: str
    started_at: str
    completed_at: Optional[str] = None
    results: Optional[List[dict]] = None

    class Config:
        from_attributes = True
