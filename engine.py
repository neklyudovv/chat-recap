import pymorphy3
from datetime import datetime
import re


def analyze_words(messages, chatter_name, threshold=0.75):
    morph = pymorphy3.MorphAnalyzer(lang='ru')
    used_words = {}
    for message in messages:
        if message['text_entities']:
            if message['from'] == chatter_name:
                for word in message['text_entities'][0]['text'].split():
                    word = re.sub(r'[^\w\s]', '', word.lower())
                    if len(word) > 4:
                        if word in used_words:
                            used_words[word] += 1
                        else:
                            p = morph.parse(word)
                            if p[0].score >= threshold:
                                used_words[word] = 1

    return dict(sorted(used_words.items(), key=lambda item: item[1], reverse=True))
    # return used_words
    # return dict(sorted(used_words.items(), key=lambda item: item[1], reverse=True))


def count_messages(messages, chatter_name):
    chatter_messages_count = 0
    for message in messages:
        if message['text_entities']:
            if message['from'] == chatter_name:
                chatter_messages_count += 1
    return chatter_messages_count


def calculate_avg_response_time(messages, chatter_name):
    response_time = []
    previous_message = messages[0]

    for message in messages[1:]:
        if message['text_entities']:
            if message['from'] != previous_message['from']:
                if message['from'] == chatter_name:
                    last_time = datetime.fromisoformat(previous_message['date'])
                    current_time = datetime.fromisoformat(message['date'])
                    diff = (current_time - last_time).total_seconds()
                    response_time.append(diff)

            previous_message = message

    return round(sum(response_time) / len(response_time), 2) if response_time else 0
