from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class Session(BaseModel):
    id: int
    user_id: int
    flashcard_ids: List[int]
    status: str  # "active", "completed", "cancelled"
    started_at: datetime
    completed_at: datetime = None
    results: List[dict] = None  # List of dicts with card_id and score
