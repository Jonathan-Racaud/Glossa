import uuid

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Flashcard(BaseModel):
    id: uuid.UUID
    front: str
    back: str
    language: str
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_studied: Optional[datetime] = None
    next_study: Optional[datetime] = None

class FlashcardCreate(BaseModel):
    front: str
    back: str
    language: str
    image_url: Optional[str] = None
    audio_url: Optional[str] = None

class FlashcardUpdate(BaseModel):
    front: Optional[str] = None
    back: Optional[str] = None
    language: Optional[str] = None
    image_url: Optional[str] = None
    audio_url: Optional[str] = None

class FlashcardResponse(BaseModel):
    id: uuid.UUID
    front: str
    back: str
    language: str
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_studied: Optional[datetime] = None
    next_study: Optional[datetime] = None

    class Config:
        from_attributes = True
