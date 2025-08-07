import json
import logging
import os
import uuid

from datetime import datetime
from typing import List
from .models import (
    Flashcard,
    FlashcardCreate, FlashcardUpdate, FlashcardResponse,
    FlashcardListResponse
)
from constants import *
from utilities import sanitize_filename

def create_flashcard(flashcard: FlashcardCreate) -> FlashcardResponse:
    """Create a new flashcard"""
    try:
        id = uuid.uuid4()
        logging.info(f"Created uuid: {id}")

        new_flashcard = Flashcard(
            id=id,
            front=flashcard.front,
            back=flashcard.back,
            language=flashcard.language,
            audio_url=flashcard.audio_url,
            image_url=flashcard.image_url,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_studied=None,
            next_study=None
        )

        logging.info(f"Created flashcard: {new_flashcard}")

        filename = sanitize_filename(str(new_flashcard.id))
        file_path = os.path.join(FLASHCARDS_DIR, filename)

        with open(file_path, "w") as f:
            json.dump(new_flashcard.model_dump(), f, default=str)

        logging.info("Written flashcard file")

        return FlashcardResponse.model_validate(new_flashcard)
    except Exception as e:
        logging.error(f"[ERROR]: {e}")
        raise e

def get_flashcard(card_id: str) -> FlashcardResponse:
    """Retrieve a specific flash card by its ID"""
    filename = sanitize_filename(card_id)
    file_path = os.path.join(FLASHCARDS_DIR, filename)

    with open(file_path, "r") as f:
        flashcard_json = json.load(f)
        flashcard = Flashcard.model_validate(flashcard_json)
        return FlashcardResponse.model_validate(flashcard)

def update_flashcard(updated_card: FlashcardUpdate) -> FlashcardResponse:
    """Update an existing flashcard"""
    try:
        filename = sanitize_filename(str(updated_card.id))
        file_path = os.path.join(FLASHCARDS_DIR, filename)

        with open(file_path, "r") as f:
            flashcard_json = json.load(f)
            flashcard = Flashcard.model_validate(flashcard_json)

        flashcard.front = updated_card.front if updated_card.front is not None else flashcard.front
        flashcard.back = updated_card.back if updated_card.back is not None else flashcard.back
        flashcard.language = updated_card.language if updated_card.language is not None else flashcard.language
        flashcard.audio_url = updated_card.audio_url if updated_card.audio_url is not None else flashcard.audio_url
        flashcard.image_url = updated_card.image_url if updated_card.image_url is not None else flashcard.image_url
        flashcard.updated_at = datetime.now()

        with open(file_path, "w") as f:
            json.dump(flashcard.model_dump(), f, default=str)

        logging.info("Updated flashcard file")

        return FlashcardResponse.model_validate(flashcard)
    except Exception as e:
        logging.error(f"[ERROR]: {e}")
        raise e

def delete_flashcard(id: uuid.UUID) -> FlashcardResponse:
    """Delete a flashcard by its ID"""
    try:
        filename = sanitize_filename(str(id))
        file_path = os.path.join(FLASHCARDS_DIR, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info("Deleted flashcard file")
            return FlashcardResponse(id=id, front="", back="", language="", audio_url="", image_url="", created_at=datetime.now(), updated_at=datetime.now(), last_studied=None, next_study=None)
        else:
            logging.error("Flashcard file not found")
            raise FileNotFoundError("Flashcard file not found")
    except Exception as e:
        logging.error(f"[ERROR]: {e}")
        raise e

def list_flashcards() -> FlashcardListResponse:
    """List all flashcards"""
    try:
        flashcards: List[Flashcard] = []
        for filename in os.listdir(FLASHCARDS_DIR):
            if filename.endswith(".json"):
                file_path = os.path.join(FLASHCARDS_DIR, filename)
                with open(file_path, "r") as f:
                    flashcard_json = json.load(f)
                    flashcard = Flashcard.model_validate(flashcard_json)
                    flashcards.append(flashcard)

        print(flashcards)
        return FlashcardListResponse(cards=flashcards)
    except Exception as e:
        logging.error(f"[ERROR]: {e}")
        raise e

flashcards_tools = [
    create_flashcard,
    update_flashcard,
    get_flashcard,
    delete_flashcard,
    list_flashcards
]
