import matplotlib.pyplot as plt
import math

from config import COLORS, DEFAULT_FIG_SIZE, MIN_MESSAGES_THRESHOLD

def render_recap(results: dict, output_path, top_n: int = 5):
    # filter top n active users
    # sort chatters by message count
    sorted_chatters = sorted(
        results.keys(), 
        key=lambda x: results[x]['messages_count'], 
        reverse=True
    )
    
    if len(sorted_chatters) > top_n:
        top_chatters = sorted_chatters[:top_n]
        print(f"Showing top {top_n} chatters out of {len(sorted_chatters)}.")
    else:
        top_chatters = sorted_chatters

    # prepare data for plotting
    names = [results[c]['name'] for c in top_chatters]
    counts = [results[c]['messages_count'] for c in top_chatters]
    avg_times = [results[c]['avg_time'] for c in top_chatters]
    
    num_word_plots = len(top_chatters)
    cols_per_row = 2
    word_plot_rows = math.ceil(num_word_plots / cols_per_row)
    
    total_rows = 1 + word_plot_rows
    
    # increase height based on rows
    fig_height = 6 + (4 * word_plot_rows) 
    fig, axes = plt.subplots(total_rows, cols_per_row, figsize=(12, fig_height))
    
    # flatten axes for easier access if it's 2D array, but handle 1D case
    if total_rows == 1:
        axes = [axes]
    
    # ax 0,0 -> messages
    ax_msg = axes[0, 0] if total_rows > 1 else axes[0]
    ax_msg.bar(names, counts, color=COLORS[:len(names)])
    ax_msg.set_title("Messages Count")
    ax_msg.tick_params(axis='x', rotation=45)

    # ax 0,1 -> avg time
    ax_time = axes[0, 1] if total_rows > 1 else axes[1]
    ax_time.bar(names, avg_times, color=COLORS[:len(names)])
    ax_time.set_title("Avg Response Time (s)")
    ax_time.tick_params(axis='x', rotation=45)

    # iterate over axes starting from row 1
    chart_idx = 0
    for i in range(1, total_rows):
        for j in range(cols_per_row):
            if chart_idx >= num_word_plots:
                # disable extra axes
                axes[i, j].axis('off')
                continue
            
            chatter = top_chatters[chart_idx]
            word_stats = results[chatter]['word_stats']
            
            ax = axes[i, j]
            if word_stats:
                words = list(word_stats.keys())[::-1]
                freqs = list(word_stats.values())[::-1]
                ax.barh(words, freqs, color=COLORS[chart_idx % len(COLORS)])
                ax.set_title(f"Most Used Words - {chatter}")
            else:
                ax.text(0.5, 0.5, "Not enough data", ha='center')
                ax.set_title(f"Most Used Words - {chatter}")
            
            chart_idx += 1
            
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Saved visualization to {output_path}")
