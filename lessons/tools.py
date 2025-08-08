import json
import logging
import os
import uuid

from datetime import datetime
from typing import List

from .models import (
    Lesson,
    LessonCreate, LessonUpdate,
    LessonResponse, LessonDeleteResponse, LessonListResponse
)

from constants import LESSONS_DIR
from utilities import sanitize_filename

def create_lesson(lesson: LessonCreate) -> LessonResponse:
    """Create a new lesson"""
    try:
        id = uuid.uuid4()

        new_lesson = Lesson(
            id=id,
            title=lesson.title,
            content=lesson.content,
            date=datetime.now()
        )

        filename = sanitize_filename(new_lesson.title)
        file_path = os.path.join(LESSONS_DIR, filename)

        with open(file_path, "w") as f:
            json.dump(new_lesson.model_dump(), f, default=str)

        return LessonResponse.model_validate(new_lesson)
    except Exception as e:
        raise e

def get_lesson(lesson_title: str) -> LessonResponse:
    """Retrieve a specific lesson by its title"""
    filename = sanitize_filename(lesson_title)
    file_path = os.path.join(LESSONS_DIR, filename)

    with open(file_path, "r") as f:
        lesson_json = json.load(f)
        lesson = Lesson.model_validate(lesson_json)
        return LessonResponse(lesson=lesson)

def update_lesson(updated_card: LessonUpdate) -> LessonResponse:
    """Update an existing lesson"""
    try:
        filename = sanitize_filename(updated_card.title)
        file_path = os.path.join(LESSONS_DIR, filename)

        with open(file_path, "r") as f:
            lesson_json = json.load(f)
            lesson = Lesson.model_validate(lesson_json)

        lesson.title = updated_card.title if updated_card.title is not None else lesson.title
        lesson.content = updated_card.content if updated_card.content is not None else lesson.content

        with open(file_path, "w") as f:
            json.dump(lesson.model_dump(), f, default=str)

        logging.info("Updated lesson file")

        return LessonResponse.model_validate(lesson)
    except Exception as e:
        logging.error(f"[ERROR]: {e}")
        raise e

def delete_lesson(title: str) -> LessonDeleteResponse:
    """Delete a lesson by its ID"""
    try:
        filename = sanitize_filename(title)
        file_path = os.path.join(LESSONS_DIR, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info("Deleted lesson file")
            return LessonDeleteResponse(status="success", message=f"Successfully deleted lesson: {title}")
        else:
            logging.error("Flashcard file not found")
            raise FileNotFoundError("Flashcard file not found")
    except Exception as e:
        logging.error(f"[ERROR]: {e}")
        raise e

def list_lessons() -> LessonListResponse:
    """List all lessons"""
    try:
        lessons: List[str] = []
        for filename in os.listdir(LESSONS_DIR):
            if filename.endswith(".json"):
                lesson_title = filename.removesuffix(".json")
                lessons.append(lesson_title)
        return LessonListResponse(lessons=lessons)
    except Exception as e:
        logging.error(f"[ERROR]: {e}")
        raise e

lessons_tools = [
    create_lesson,
    update_lesson,
    get_lesson,
    delete_lesson,
    list_lessons
]
