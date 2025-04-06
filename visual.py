import matplotlib.pyplot as plt
import warnings


def render_recap(results):
    warnings.filterwarnings("ignore")
    fig, axes = plt.subplots(2, 2, figsize=(10, 12))

    # Messages count
    axes[0, 0].bar([results[chatter]['name'] for chatter in results],
                   [results[chatter]['messages_count'] for chatter in results],
                   color=["#FF5722", "#405DE6"])
    axes[0, 0].set_title("Messages Count")

    # Average response time
    axes[0, 1].bar([results[chatter]['name'] for chatter in results],
                   [results[chatter]['avg_time'] for chatter in results],
                   color=["#FF5722", "#405DE6"])
    axes[0, 1].set_title("Avg Response Time (s)")

    # Most used words
    for i, chatter in enumerate(results):
        if i > 1:
            break

        axes[1, i].barh(list(results[chatter]['word_stats'].keys())[::-1],
                        list(results[chatter]['word_stats'].values())[::-1],
                        color="#FF5722" if i == 0 else "#405DE6")
        axes[1, i].set_title(f"Most Used Words - {results[chatter]['name']}")

    plt.tight_layout(rect=(0, 0, 1, 0.96))
    plt.savefig("chat_recap.png")
    print("Saved as chat_recap.png")
