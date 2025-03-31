import json
import pandas as pd


def load_chat_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if "messages" not in data or "name" not in data:
            raise ValueError("wrong data format")

        df = pd.DataFrame(data["messages"])
        df = df[df["type"] == "message"].copy()

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

        return df

    except FileNotFoundError:
        raise ValueError("no such file")
    except json.JSONDecodeError:
        raise ValueError("incorrect json")
