from models.flashcard import Flashcard

def sanitize_filename(flashcard_name: str) -> str:
    filename = str(flashcard_name).replace(" ", "_").replace("/", "_").replace("\\", "_")
    
    if not filename:
        return {"error": "Wrong flashcard format"}
    
    # Ensure the filename ends with .json
    if not filename.lower().endswith(".json"):
        filename += ".json"
    
    return filename