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
    """Create a new flashcard with the given front and back content"""
    # Create the directory if it doesn't exist
    if not os.path.exists(FLASHCARDS_DIR):
        os.makedirs(FLASHCARDS_DIR)
    
    # Use the front text as the filename (sanitized to be a valid filename)
    filename = flashcard.front.strip().replace(" ", "_").replace("/", "_").replace("\\", "_")
    if not filename:
        filename = "unknown_flashcard"
    
    # Ensure the filename ends with .json
    if not filename.lower().endswith(".json"):
        filename += ".json"
    
    # Full path to the flashcard file
    file_path = os.path.join(FLASHCARDS_DIR, filename)
    
    # Check if a flashcard with this front already exists
    if os.path.exists(file_path):
        raise FileExistsError(f"A flashcard with the front '{flashcard.front}' already exists.")
    
    # Create the flashcard object
    new_flashcard = Flashcard(
        front=flashcard.front,
        back=flashcard.back,
        id=None  # Will be assigned by the system
    )
    
    # Write the flashcard to file
    try:
        with open(file_path, "w") as f:
            json.dump(new_flashcard.model_dump(), f, indent=2)
        logging.info(f"Created new flashcard: {flashcard.front}")
        return {"message": f"Flashcard '{flashcard.front}' created successfully", "filename": filename}
    except Exception as e:
        logging.error(f"Failed to create flashcard: {e}")
        raise

if __name__ == "__main__":
    if not os.path.exists(FLASHCARDS_DIR):
        os.makedirs(FLASHCARDS_DIR)

    mcp.run(transport="streamable-http")
