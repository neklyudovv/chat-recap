import matplotlib.pyplot as plt


def render_recap(your_name, chatter_name, your_messages_count, chatter_messages_count,
                 your_average_time, chatter_average_time, your_word_stats, chatter_word_stats,
                 your_emoji_stats, chatter_emoji_stats):
    fig, axes = plt.subplots(3, 2, figsize=(8, 12))

    # Messages count
    axes[0, 0].bar([your_name, chatter_name], [your_messages_count, chatter_messages_count],
                   color=["#FF5722", "#405DE6"])
    axes[0, 0].set_title("Messages Count")

    # Average response time
    axes[0, 1].bar([your_name, chatter_name], [your_average_time, chatter_average_time], color=["#FF5722", "#405DE6"])
    axes[0, 1].set_title("Avg Response Time (s)")

    your_words, your_counts = zip(*sorted(your_word_stats, key=lambda x: x[1], reverse=True))
    chatter_words, chatter_counts = zip(*sorted(chatter_word_stats, key=lambda x: x[1], reverse=True))

    axes[1, 0].barh(your_words[:5][::-1], your_counts[:5][::-1], color="#FF5722")
    axes[1, 0].set_title(f"Most Used Words - {your_name}")

    axes[1, 1].barh(chatter_words[:5][::-1], chatter_counts[:5][::-1], color="#405DE6")
    axes[1, 1].set_title(f"Most Used Words - {chatter_name}")

    # Most used emojis
    if your_emoji_stats:
        your_emojis, your_emoji_counts = zip(*sorted(your_emoji_stats, key=lambda x: x[1], reverse=True))
        axes[2, 0].barh(your_emojis[:5][::-1], your_emoji_counts[:5][::-1], color="#FF5722")
        axes[2, 0].set_title(f"Most Used Emojis - {your_name}")

    if chatter_emoji_stats:
        chatter_emojis, chatter_emoji_counts = zip(
            *sorted(chatter_emoji_stats, key=lambda x: x[1], reverse=True))
        axes[2, 1].barh(chatter_emojis[:5][::-1], chatter_emoji_counts[:5][::-1], color="#405DE6")
        axes[2, 1].set_title(f"Most Used Emojis - {chatter_name}")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig("chat_recap.png")
    print("Saved as chat_recap.png")