from datetime import timedelta


from emoji import is_emoji

import pandas as pd
from src.models import Message
from config import MIN_WORD_LENGTH

class ChatAnalyzer:
    def __init__(self, messages: list[Message]):
        self.messages = messages
        # convert to DataFrame for easier time calculations
        data = [
            {
                "from": msg.from_user,
                "date": msg.date,
                "text": msg.clean_text,
                "text_entities": msg.text_entities
            }
            for msg in messages
        ]
        self.df = pd.DataFrame(data)

        if not self.df.empty:
            self.df["date"] = pd.to_datetime(self.df["date"])
            self.df.sort_values("date", inplace=True)

    def get_chatters(self) -> list[str]:
        if self.df.empty:
            return []
        return sorted(self.df["from"].dropna().unique().tolist())

    def analyze_words(self, chatter_name: str) -> dict:
        if self.df.empty: 
            return {}
        
        text_series = self.df.loc[self.df["from"] == chatter_name, "text"].dropna()
        # find words using regex (considering min length from config)
        pattern = fr"\b\w{{{MIN_WORD_LENGTH},}}\b" 
        words = text_series.str.lower().str.findall(pattern).explode()
        
        if words.empty:
            return {}
            
        return words.value_counts().head(10).to_dict()

    def analyze_emojis(self, chatter_name: str) -> dict:
        # extract emojis directly from text
        text_series = self.df.loc[self.df["from"] == chatter_name, "text"].dropna()
        
        all_emojis = []
        for text in text_series:
            all_emojis.extend([char for char in text if is_emoji(char)])
            
        if not all_emojis:
            return {}
        return pd.Series(all_emojis).value_counts().head(10).to_dict()

    def count_messages(self, chatter_name: str) -> int:
        if self.df.empty:
            return 0
        return self.df[self.df["from"] == chatter_name].shape[0]

    def calculate_avg_response_time(self, chatter_name: str) -> float:
        if self.df.empty:
            return 0.0
            
        # filter only necessary columns
        df_filtered = self.df[["from", "date"]].dropna().sort_values("date")
        df_filtered["prev_from"] = df_filtered["from"].shift(1)
        df_filtered["prev_date"] = df_filtered["date"].shift(1)

        # calculate response time: if previous message was NOT from us
        mask = (df_filtered["from"] == chatter_name) & (df_filtered["prev_from"] != chatter_name) & (df_filtered["prev_from"].notna())
        response_times = (df_filtered["date"] - df_filtered["prev_date"])[mask].dt.total_seconds()

        return round(response_times.mean(), 2) if not response_times.empty else 0.0

    # additional metrics
    def get_most_active_period(self, days: int = 7):
        if self.df.empty:
            return None
            
        curr_date = self.df["date"].dt.date
        period_start = curr_date - pd.to_timedelta(curr_date.apply(lambda d: d.day % days), unit="D")
        activity = period_start.value_counts().sort_values(ascending=False)

        if activity.empty:
            return None

        most_active_start = activity.idxmax()
        return {
            "start": most_active_start,
            "end": most_active_start + timedelta(days=days - 1),
            "messages_count": activity.max(),
        }

    def get_top_initiators(self, gap_minutes: int = 30) -> dict:
        if self.df.empty:
            return {}
            
        df = self.df[["from", "date"]].copy().sort_values("date")
        df["time_diff"] = df["date"].diff().dt.total_seconds()
        gap_seconds = gap_minutes * 60
        
        # new dialogue if gap > threshold or it's the first message
        df["new_dialogue"] = (df["time_diff"] > gap_seconds) | (df["time_diff"].isna())

        initiators = df.loc[df["new_dialogue"], "from"]
        return initiators.value_counts().to_dict()

    def get_stats(self):
        result = {}
        for chatter in self.get_chatters():
            result[chatter] = {
                'name': chatter,
                'word_stats': self.analyze_words(chatter),
                'messages_count': self.count_messages(chatter),
                'avg_time': self.calculate_avg_response_time(chatter),
                'emojis': self.analyze_emojis(chatter),
            }
        return result
