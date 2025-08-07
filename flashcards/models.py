import uuid

from datetime import datetime, timezone
from typing import Optional, List
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

    class Config:
        json_encoders = {
            # We need to have timezone aware datetime otherwise the schema validation fails
            datetime: lambda dt: dt.astimezone(timezone.utc).isoformat(timespec="milliseconds") if dt else None
        }

class FlashcardCreate(BaseModel):
    front: str
    back: str
    language: str
    image_url: Optional[str] = None
    audio_url: Optional[str] = None

class FlashcardUpdate(BaseModel):
    id: uuid.UUID
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
        json_encoders = {
            # We need to have timezone aware datetime otherwise the schema validation fails
            datetime: lambda dt: dt.astimezone(timezone.utc).isoformat(timespec="milliseconds") if dt else None
        }

class FlashcardListResponse(BaseModel):
    cards: List[Flashcard]
