import os
import json
import logging
import uuid
from datetime import datetime

from typing import Dict
from dataclasses import asdict
from mcp.server.fastmcp import FastMCP

from models.flashcard import Flashcard
from schemas.flashcard import FlashcardCreate, FlashcardResponse
from utilities import sanitize_filename
from constants import *

mcp = FastMCP("StatefulServer")

@mcp.tool()
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

        filename = sanitize_filename(new_flashcard.id)
        file_path = os.path.join(FLASHCARDS_DIR, filename)

        with open(file_path, "w") as f:
            json.dump(new_flashcard.model_dump(), f, default=str)
        
        logging.info("Written flashcard file")

        return FlashcardResponse.model_validate(new_flashcard)
    except Exception as e:
        logging.error(f"[ERROR]: {e}")
        raise e

@mcp.tool()
def get_flashcard(card_id: str) -> FlashcardResponse:
    """Retrieve a specific flash card by its ID"""
    filename = sanitize_filename(card_id)
    file_path = os.path.join(FLASHCARDS_DIR, filename)

    with open(file_path, "r") as f:
        flashcard_json = json.load(f)
        flashcard = Flashcard.model_validate(flashcard_json)
        return FlashcardResponse.model_validate(flashcard)

if __name__ == "__main__":
    if not os.path.exists(FLASHCARDS_DIR):
        os.makedirs(FLASHCARDS_DIR)

    mcp.run(transport="streamable-http")
