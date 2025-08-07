def sanitize_filename(flashcard_name: str) -> str:
    filename = flashcard_name.replace(" ", "_").replace("/", "_").replace("\\", "_")

    # Ensure the filename ends with .json
    if not filename.lower().endswith(".json"):
        filename += ".json"

    return filename
