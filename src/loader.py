import json

from src.models import ChatExport, Message
from config import DATA_DIR

def load_chat_data(file_path) -> [Message]:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {file_path}: {e}")

    try:
        # validate structure with pydantic
        chat_export = ChatExport(**data)
    except Exception as e:
        raise ValueError(f"Data validation error: {e}")

    # filter for valid messages only
    valid_messages = [
        msg for msg in chat_export.messages 
        if msg.type == 'message' and msg.date is not None
    ]

    return valid_messages
