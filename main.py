import json
from engine import analyze_words, count_messages, calculate_avg_response_time, analyze_emojis, get_your_name
from utils import format_word_stats
from visual import render_recap


def main():
    f = open("result.json", 'r')
    data = json.load(f)
    f.close()

    messages = data['messages']
    chatter_name = data['name']
    your_name = get_your_name(messages, chatter_name)
    your_word_stats = analyze_words(messages, your_name)
    chatter_word_stats = analyze_words(messages, chatter_name)
    chatter_messages_count = count_messages(messages, chatter_name)
    your_messages_count = len(messages)-chatter_messages_count
    your_average_time = calculate_avg_response_time(messages, your_name)
    chatter_average_time = calculate_avg_response_time(messages, chatter_name)

    print('chatter:', chatter_name)
    print('total messages count:', len(messages))
    print(f'most used words:\n{your_name}: {format_word_stats(your_word_stats)}'
          f'{chatter_name} {format_word_stats(chatter_word_stats)}')
    print(f'messages sent:\n{your_name}: {your_messages_count}'
          f' {chatter_name}: {chatter_messages_count}')
    print(f'avg response times (s):\n{your_name}: {your_average_time}'
          f' {chatter_name}: {chatter_average_time}')

    render_recap(your_name, chatter_name, your_messages_count,
                 chatter_messages_count, your_average_time, chatter_average_time,
                 your_word_stats, chatter_word_stats)
    print(format_word_stats(analyze_emojis(messages, your_name)))
    print(format_word_stats(analyze_emojis(messages, chatter_name)))


if __name__ == "__main__":
    main()
