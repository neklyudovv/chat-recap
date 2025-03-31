from data_loader import load_chat_data
from engine import ChatAnalyzer
from visual import render_recap


def main():
    data = load_chat_data("result.json")  # pandas data, not json data

    analyzer = ChatAnalyzer(data)
    results = analyzer.get_stats()
    # print(results)  # по сути results это уже готовый ответ, по которому можно рисовать картинку
    # / отдавать на сайт в качестве ответа

    print('chatter:', analyzer.chatter_name)
    print('total messages:', len(analyzer.df))
    print(f'most used words:\n{analyzer.your_name}: {results["your_word_stats"]}\n'
          f'{analyzer.chatter_name}: {results["chatter_word_stats"]}')
    print(f'messages sent:\n{analyzer.your_name}: {results["your_messages_count"]}\n'
          f'{analyzer.chatter_name}: {results["chatter_messages_count"]}')
    print(f'avg response times (s):\n{analyzer.your_name}: {results["your_average_time"]}\n'
          f'{analyzer.chatter_name}: {results["chatter_average_time"]}')
    print(f'most used emojis:\n{analyzer.your_name}: {results["your_emojis"]}\n'
          f'{analyzer.chatter_name}: {results["chatter_emojis"]}')
    print(f'most active month: from {results["most_active_month"]["start"]} to '
          f'{results["most_active_month"]["end"]} with msg count of {results["most_active_month"]["messages_count"]}')

    render_recap(analyzer.your_name, analyzer.chatter_name, results['your_messages_count'],
                 results['chatter_messages_count'], results['your_average_time'],
                 results['chatter_average_time'], results['your_word_stats'],
                 results['chatter_word_stats'])


if __name__ == "__main__":
    main()
