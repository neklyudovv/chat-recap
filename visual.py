import matplotlib.pyplot as plt
import warnings


def render_recap(your_name, chatter_name, your_messages_count, chatter_messages_count,
                 your_average_time, chatter_average_time, your_word_stats, chatter_word_stats):
    warnings.filterwarnings("ignore")
    fig, axes = plt.subplots(2, 2, figsize=(10, 12))

    # Messages count
    axes[0, 0].bar([your_name, chatter_name], [your_messages_count, chatter_messages_count],
                   color=["#FF5722", "#405DE6"])
    axes[0, 0].set_title("Messages Count")

    # Average response time
    axes[0, 1].bar([your_name, chatter_name], [your_average_time, chatter_average_time],
                   color=["#FF5722", "#405DE6"])
    axes[0, 1].set_title("Avg Response Time (s)")

    # Most used words
    axes[1, 0].barh(list(your_word_stats.keys())[::-1], list(your_word_stats.values())[::-1], color="#FF5722")
    axes[1, 0].set_title(f"Most Used Words - {your_name}")

    axes[1, 1].barh(list(chatter_word_stats.keys())[::-1], list(chatter_word_stats.values())[::-1], color="#405DE6")
    axes[1, 1].set_title(f"Most Used Words - {chatter_name}")

    plt.tight_layout(rect=(0, 0, 1, 0.96))
    plt.savefig("chat_recap.png")
    print("Saved as chat_recap.png")
