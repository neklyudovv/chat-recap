import json


def load_chat_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if "messages" not in data or "name" not in data:
            raise ValueError("wrong data format")
        return data

    except FileNotFoundError:
        raise ValueError("no such file")
    except json.JSONDecodeError:
        raise ValueError("incorrect json")
