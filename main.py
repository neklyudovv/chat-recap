import json
import pymorphy3
from datetime import datetime


def analyze_words(messages, threshold=0.75):
    morph = pymorphy3.MorphAnalyzer(lang='ru')
    used_words = {}
    for message in messages:
        if message['text_entities']:
            for word in message['text_entities'][0]['text'].split():
                word = word.lower()
                # if score >= threshold and len(word)>4:
                if len(word) > 4:
                    if word in used_words:
                        used_words[word] += 1
                    else:
                        p = morph.parse(word)
                        if p[0].score >= threshold:
                            used_words[word] = 1
    return dict(sorted(used_words.items(), key=lambda item: item[1], reverse=True))


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
                if message['from'] == chatter_name:  # dont want to hardcode usernames so..
                    response_time[1].append(diff)
                else:
                    response_time[0].append(diff)

            previous_message = message

    avg_response_time = {}
    for author, times in response_time.items():
        avg_response_time[author] = round(sum(times) / len(times), 2) if times else 0

    return avg_response_time


def main():
    f = open("result.json", 'r')
    data = json.load(f)
    chatter_name = data['name']
    your_name = next((message['from'] for message in data['messages'] if message['from'] != chatter_name), chatter_name)
    print('chatter:', chatter_name)
    print('total messages count:', len(data['messages']))

    messages = data['messages']
    word_stats = analyze_words(messages)
    your_messages_count, chatter_messages_count = count_messages(messages, chatter_name)
    average_times = calculate_avg_response_time(messages, chatter_name)

    print('most used words:')
    for i, word in enumerate(word_stats):
        if i < 10:
            print(word, word_stats[word])

    print(f'messages sent:\n{your_name}: {your_messages_count}'
          f' {chatter_name}: {chatter_messages_count}')
    print(f'avg response times (s):\n{your_name}: {average_times[0]}'
          f' {chatter_name}: {average_times[1]}')

    f.close()


if __name__ == "__main__":
    main()
