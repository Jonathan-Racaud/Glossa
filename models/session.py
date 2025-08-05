from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class Session(BaseModel):
    id: int
    user_id: int
    flashcard_ids: List[int]
    status: str  # "active", "completed", "cancelled"
    started_at: datetime
    completed_at: Optional[datetime] = None
    results: Optional[List[dict]] = None  # List of dicts with card_id and score
