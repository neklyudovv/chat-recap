from data_loader import load_chat_data
from engine import ChatAnalyzer
from visual import render_recap


def main():
    data = load_chat_data("result.json")  # pandas data, not json data

    analyzer = ChatAnalyzer(data)
    results = analyzer.get_stats()
    # print(results)  # по сути results это уже готовый ответ, по которому можно рисовать картинку
    # / отдавать на сайт в качестве ответа
    sections = {
        "most used words": "word_stats",
        "messages sent": "messages_count",
        "avg response time (s)": "avg_time",
        "most used emojis": "emojis",
    }

    print('total messages:', len(analyzer.df))
    for section, key in sections.items():
        print(section + ":")
        for chatter, data in results.items():
            print(f"{data['name']}: {data[key]}")

    render_recap(results)


if __name__ == "__main__":
    main()
