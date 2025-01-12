import pymorphy3
from datetime import datetime


def analyze_words(messages, chatter_name, threshold=0.75):
    morph = pymorphy3.MorphAnalyzer(lang='ru')
    used_words = [{}, {}]
    for message in messages:
        if message['text_entities']:
            for word in message['text_entities'][0]['text'].split():
                word = word.lower()
                # if score >= threshold and len(word)>4:
                if len(word) > 4:
                    index = 1 if message['from'] == chatter_name else 0
                    if word in used_words[index]:
                        used_words[index][word] += 1
                    else:
                        p = morph.parse(word)
                        if p[0].score >= threshold:
                            used_words[index][word] = 1

    return [dict(sorted(used_words[0].items(), key=lambda item: item[1], reverse=True)),
            dict(sorted(used_words[1].items(), key=lambda item: item[1], reverse=True))]
    # return used_words
    # return dict(sorted(used_words.items(), key=lambda item: item[1], reverse=True))


def count_messages(messages, chatter_name):
    chatter_messages_count = 0
    for message in messages:
        if message['text_entities']:
            if message['from'] == chatter_name:
                chatter_messages_count += 1
    return len(messages) - chatter_messages_count, chatter_messages_count


def calculate_avg_response_time(messages, chatter_name):
    response_time = {0: [], 1: []}
    previous_message = messages[0]

    for message in messages[1:]:
        if message['text_entities']:
            if message['from'] != previous_message['from']:
                last_time = datetime.fromisoformat(previous_message['date'])
                current_time = datetime.fromisoformat(message['date'])
                diff = (current_time - last_time).total_seconds()
                index = 1 if message['from'] == chatter_name else 0
                response_time[index].append(diff)

            previous_message = message

    avg_response_time = {}
    for author, times in response_time.items():
        avg_response_time[author] = round(sum(times) / len(times), 2) if times else 0

    return avg_response_time
