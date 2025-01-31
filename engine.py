from datetime import datetime, timedelta
from emoji import is_emoji
import re


class ChatAnalyzer:
    def __init__(self, data):
        self.messages = data['messages']
        self.chatter_name = data['name']
        self.your_name = self.get_your_name()

    def get_your_name(self):
        return next((message['from'] for message in self.messages if message['text_entities']
                     and message['from'] != self.chatter_name), self.chatter_name)

    def analyze_words(self, chatter_name):
        used_words = {}
        for message in self.messages:
            if message['text_entities'] and message['from'] == chatter_name:
                text = message['text_entities'][0]['text'].lower()
                for word in re.findall(r'\b\w{5,}\b', text):
                    used_words[word] = used_words.get(word, 0) + 1

        return sorted(used_words.items(), key=lambda item: item[1], reverse=True)

    def analyze_emojis(self, chatter_name):
        used_emojis = {}
        for message in self.messages:
            if message['text_entities'] and message['from'] == chatter_name:
                for char in message['text_entities'][0]['text']:
                    if is_emoji(char):
                        used_emojis[char] = used_emojis.get(char, 0) + 1

        return sorted(used_emojis.items(), key=lambda item: item[1], reverse=True)

    def count_messages(self, chatter_name):
        return sum(1 for message in self.messages if "from" in message and message['from'] == chatter_name)

    def calculate_avg_response_time(self, chatter_name):
        response_time = []
        previous_message = None
        for message in self.messages:
            if "from" in message:
                previous_message = message
                break
        if previous_message is None:
            return -1

        for message in self.messages:
            if "from" in message:
                if message['from'] != previous_message['from']:
                    if message['from'] == chatter_name:
                        last_time = datetime.fromisoformat(previous_message['date'])
                        current_time = datetime.fromisoformat(message['date'])
                        diff = (current_time - last_time).total_seconds()
                        response_time.append(diff)

                previous_message = message

        return round(sum(response_time) / len(response_time), 2) if response_time else 0

    def most_active_period(self, days):
        activity = {}

        for message in self.messages:
            date = datetime.fromisoformat(message['date']).date()
            period_start = date - timedelta(days=date.day % days)

            activity[period_start] = activity.get(period_start, 0) + 1

        sorted_activity = sorted(activity.items(), key=lambda x: x[1], reverse=True)

        if sorted_activity:
            most_active_period_start = sorted_activity[0][0]
            most_active_period_end = most_active_period_start + timedelta(days=days - 1)
            message_count = sorted_activity[0][1]
            return {
                'start': most_active_period_start,
                'end': most_active_period_end,
                'messages_count': message_count
            }
        return None

    def get_stats(self):
        results = {
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
        return results
