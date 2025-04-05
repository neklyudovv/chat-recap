from datetime import timedelta
from emoji import is_emoji
import pandas as pd


class ChatAnalyzer:
    def __init__(self, df):
        self.df = df.copy()  # копия, чтобы не портить оригинал
        self.preprocess()
        self.chatters = self.get_chatters()

    def preprocess(self):
        # print(self.df.keys())
        if "date" in self.df.columns:
            self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
            self.df = self.df.dropna(subset=["date"])  # убираем некорректные даты

        if "from" in self.df.columns:
            self.df["from"] = self.df["from"].astype(str).str.strip()

        if "text" in self.df.columns:
            self.df = self.df[self.df["text"].apply(lambda x: isinstance(x, str))]  # теперь только строки
            self.df["text"] = (self.df["text"].str.strip().replace(r"\s+", " ", regex=True))

    def get_chatters(self):
        if "from" in self.df.columns:
            return sorted(self.df["from"].dropna().unique().tolist())
        return []

    def analyze_words(self, chatter_name):
        text_series = self.df.loc[self.df["from"] == chatter_name, "text"].dropna()
        words = text_series.str.lower().str.findall(r"\b\w{5,}\b").explode()  # len>4
        return words.value_counts().head(10).to_dict()

    def analyze_emojis(self, chatter_name):
        text_series = self.df.loc[self.df["from"] == chatter_name, "text_entities"].dropna()
        emojis = text_series.apply(
            lambda x: [char for char in x[0]['text'] if is_emoji(char)] if isinstance(x, list) and len(x) > 0 else []
        ).explode()
        return emojis.value_counts().head(10).to_dict()

    def count_messages(self, chatter_name):
        return self.df[self.df["from"] == chatter_name].shape[0]

    def calculate_avg_response_time(self, chatter_name):
        df_filtered = self.df[["from", "date"]].dropna().sort_values("date")
        df_filtered["prev_from"] = df_filtered["from"].shift(1)
        df_filtered["prev_date"] = df_filtered["date"].shift(1)

        mask = (df_filtered["from"] == chatter_name) & (df_filtered["prev_from"] != chatter_name)
        response_times = (df_filtered["date"] - df_filtered["prev_date"])[mask].dt.total_seconds()

        return round(response_times.mean(), 2) if not response_times.empty else 0

    def most_active_period(self, days):
        curr_date = pd.to_datetime(self.df["date"]).dt.date  # убрал время, только дата для правильного подсчета
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

    def get_stats(self):
        result = {}
        for chatter in self.chatters:
            result[chatter] = {
                'name': chatter,
                'word_stats': self.analyze_words(chatter),
                'messages_count': self.count_messages(chatter),
                'avg_time': self.calculate_avg_response_time(chatter),
                'emojis': self.analyze_emojis(chatter),
            }
        return result
