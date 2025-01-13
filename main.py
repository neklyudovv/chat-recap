import json
from engine import analyze_words, count_messages, calculate_avg_response_time
# from visual import render_recap


def main():
    f = open("result.json", 'r')
    data = json.load(f)
    f.close()

    messages = data['messages']
    chatter_name = data['name']
    your_name = next((message['from'] for message in messages if message['from'] != chatter_name), chatter_name)
    word_stats = analyze_words(messages, chatter_name)
    your_messages_count, chatter_messages_count = count_messages(messages, chatter_name)
    average_times = calculate_avg_response_time(messages, chatter_name)

    print('chatter:', chatter_name)
    print('total messages count:', len(messages))
    print('most used words:')

    for i in range(0, 2):
        print(your_name+':' if i == 0 else chatter_name+':')
        for j, word in enumerate(word_stats[i]):
            if j<10:
                print(word, word_stats[i][word])

    print(f'messages sent:\n{your_name}: {your_messages_count}'
          f' {chatter_name}: {chatter_messages_count}')
    print(f'avg response times (s):\n{your_name}: {average_times[0]}'
          f' {chatter_name}: {average_times[1]}')

    # render_recap(your_name, chatter_name, your_messages_count,
                 # chatter_messages_count, average_times[0], average_times[1],  word_stats)


if __name__ == "__main__":
    main()
