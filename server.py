import os
import json
import logging

from typing import List
from dataclasses import asdict
from mcp.server.fastmcp import FastMCP

from models.flashcard import Flashcard
from schemas.flashcard import FlashcardCreate

DATA_DIR = "data"
FLASHCARDS_DIR = f"{DATA_DIR}/flashcards"

mcp = FastMCP("StatefulServer")


@mcp.resource("flashcards://list")
def list_flashcards() -> List[Flashcard]:
    """List all the available flashcards"""
    flashcards: List[Flashcard] = []

    for filename in os.listdir(FLASHCARDS_DIR):
        file_path = os.path.join(FLASHCARDS_DIR, filename)

        if not os.path.isfile(file_path) and not filename.lower().endswith(".json"):
            continue
        try:
            with open(file_path, "r") as flashcard_file:
                flashcard_json = json.load(flashcard_file)
                flashcard = Flashcard.model_validate_json(flashcard_json)
                flashcards.append(flashcard)
        except Exception as e:
            logging.error(f"Couldn't read flashcard: {filename}: {e}")

@mcp.tool()
def create_flashcard(flashcard: FlashcardCreate):
    flashcard_filename = os.path.join(FLASHCARDS_DIR, flashcard.front)
    
    with open(flashcard_filename, "w"):
        json.dump(flashcard_filename, flashcard.model_dump_json())

if __name__ == "__main__":
    if not os.path.exists(FLASHCARDS_DIR):
        os.makedirs(FLASHCARDS_DIR)

    mcp.run(transport="streamable-http")
