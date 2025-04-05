from data_loader import load_chat_data
from engine import ChatAnalyzer
from visual import render_recap


def main():
    data = load_chat_data("result.json")  # pandas data, not json data

    analyzer = ChatAnalyzer(data)
    results = analyzer.get_stats()

    sections = {
        "most used words": "word_stats",
        "messages sent": "messages_count",
        "avg response time (s)": "avg_time",
        "most used emojis": "emojis",
    }
    # print(results)  # по сути results это уже готовый ответ, по которому можно рисовать картинку
    # / отдавать на сайт в качестве ответа
    print('total messages:', len(analyzer.df))
    for section, key in sections.items():
        print(section + ":")
        for chatter, data in results.items():
            print(f"{data['name']}: {data[key]}")

    # render_recap(analyzer.your_name, analyzer.chatter_name, results['your_messages_count'],
    #             results['chatter_messages_count'], results['your_average_time'],
    #             results['chatter_average_time'], results['your_word_stats'],
    #             results['chatter_word_stats'])


if __name__ == "__main__":
    main()
