from pydantic import BaseModel
from typing import Optional

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
    id: int
    front: str
    back: str
    language: str
    image_url: Optional[str] = None
    audio_url: Optional[str] = None
    created_at: str
    updated_at: str
    last_studied: Optional[str] = None
    next_study: Optional[str] = None

    class Config:
        from_attributes = True
