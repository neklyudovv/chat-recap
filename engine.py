import pymorphy3
from datetime import datetime
from emoji import is_emoji
import re


class ChatAnalyzer:
    def __init__(self, data):
        self.messages = data['messages']
        self.chatter_name = data['name']
        self.your_name = self.get_your_name()
        self.results = {}

    def get_your_name(self):
        return next((message['from'] for message in self.messages if message['text_entities']
                     and message['from'] != self.chatter_name), self.chatter_name)

    def analyze_words(self, chatter_name, threshold=0.75):
        morph = pymorphy3.MorphAnalyzer(lang='ru')
        used_words = {}
        for message in self.messages:
            if message['text_entities']:
                if message['from'] == chatter_name:
                    for i in range(0, len(message['text_entities'])):
                        for word in message['text_entities'][i]['text'].split():
                            word = re.sub(r'[^\w\s]', '', word.lower())
                            if len(word) > 4:
                                if word in used_words:
                                    used_words[word] += 1
                                else:
                                    p = morph.parse(word)
                                    if p[0].score >= threshold:
                                        used_words[word] = 1

        return sorted(used_words.items(), key=lambda item: item[1], reverse=True)

    def analyze_emojis(self, chatter_name):
        used_emojis = {}
        for message in self.messages:
            if message['text_entities']:
                if message['from'] == chatter_name:
                    text = message['text_entities'][0]['text']
                    for char in text:
                        if is_emoji(char):
                            if char in used_emojis:
                                used_emojis[char] += 1
                            else:
                                used_emojis[char] = 1
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

    def analyze(self):
        self.results = {
            'your_word_stats': self.analyze_words(self.your_name),
            'chatter_word_stats': self.analyze_words(self.chatter_name),
            'your_messages_count': self.count_messages(self.your_name),
            'chatter_messages_count': self.count_messages(self.chatter_name),
            'your_average_time': self.calculate_avg_response_time(self.your_name),
            'chatter_average_time': self.calculate_avg_response_time(self.chatter_name),
            'your_emojis': self.analyze_emojis(self.your_name),
            'chatter_emojis': self.analyze_emojis(self.chatter_name)
        }
        return self.results
