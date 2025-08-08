from token import LESS
import uuid

from datetime import datetime, timezone
from typing import List
from pydantic import BaseModel

class Lesson(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    date: datetime

    class Config:
        json_encoders = {
            # We need to have timezone aware datetime otherwise the schema validation fails
            datetime: lambda dt: dt.astimezone(timezone.utc).isoformat(timespec="milliseconds") if dt else None
        }

class LessonCreate(BaseModel):
    title: str
    content: str

class LessonUpdate(BaseModel):
    id: uuid.UUID
    title: str
    content: str

class LessonResponse(BaseModel):
    lesson: Lesson

    class Config:
        from_attributes = True

class LessonDeleteResponse(BaseModel):
    status: str
    message: str

class LessonListResponse(BaseModel):
    lessons: List[str]
