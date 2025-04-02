from datetime import timedelta
from emoji import is_emoji
import pandas as pd


class ChatAnalyzer:  # а еще по хорошему бы сделать чтобы этот класс мог обрабатывать чаты не только для 2х
    def __init__(self, df):
        self.df = df.copy()  # копия, чтобы не портить оригинал
        self.preprocess()
        self.chatter_name = self.get_chatter_name()
        self.your_name = self.get_your_name()

    def preprocess(self):
        # print(self.df.keys())
        if "date" in self.df.columns:
            self.df["date"] = pd.to_datetime(self.df["date"], errors="coerce")
            self.df = self.df.dropna(subset=["date"])  # убираем некорректные даты

        if "from" in self.df.columns:
            self.df["from"] = self.df["from"].astype(str).str.strip()

        if "text" in self.df.columns:
            self.df["text"] = (
                self.df["text"]
                .astype(str)
                .str.strip()  # лишние пробелы по краям
                .replace(r"\s+", " ", regex=True)  # лишние пробелы внутри текста
            )

    def get_chatter_name(self):
        return self.df["from"].value_counts().idxmax()

    def get_your_name(self):
        unique_names = self.df["from"].unique()
        return next(name for name in unique_names if name != self.chatter_name)

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
        curr_date = pd.to_datetime(self.df["date"].dt.date)  # убрал время, только дата для правильного подсчета
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
        return {
            'your_word_stats': self.analyze_words(self.your_name),
            'chatter_word_stats': self.analyze_words(self.chatter_name),
            'your_messages_count': self.count_messages(self.your_name),
            'chatter_messages_count': self.count_messages(self.chatter_name),
            'your_average_time': self.calculate_avg_response_time(self.your_name),
            'chatter_average_time': self.calculate_avg_response_time(self.chatter_name),
            'your_emojis': self.analyze_emojis(self.your_name),
            'chatter_emojis': self.analyze_emojis(self.chatter_name),
            'most_active_month': self.most_active_period(30)
        }
