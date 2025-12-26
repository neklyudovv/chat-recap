import argparse
import sys
from pathlib import Path
from src.loader import load_chat_data
from src.analyzer import ChatAnalyzer
from src.visual import render_recap
from config import DATA_DIR, OUTPUT_DIR, OUTPUT_FILENAME

def main():
    parser = argparse.ArgumentParser(description="Telegram Chat Recap Generator")
    parser.add_argument("--input", "-i", type=str, default=str(DATA_DIR / "result.json"), help="Path to input JSON file")
    parser.add_argument("--output", "-o", type=str, default=str(OUTPUT_DIR / OUTPUT_FILENAME), help="Path to output image")
    parser.add_argument("--top_n", "-n", type=int, default=2, help="Number of top active users to show")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    # ensure output dir exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Loading data from {input_path}...")
    try:
        messages = load_chat_data(input_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)
        
    print(f"Loaded {len(messages)} valid messages.")
    
    print("Analyzing data...")
    analyzer = ChatAnalyzer(messages)
    stats = analyzer.get_stats()
    
    # metrics
    print("\n--- Metrics ---")
    print("Global:")
    print(f"  Total Messages: {len(messages)}")
    active_period = analyzer.get_most_active_period()
    if active_period:
        print(f"  Most Active Period: {active_period['start']} to {active_period['end']} ({active_period['messages_count']} msgs)")
    
    print("\nUser Stats:")
    initiators = analyzer.get_top_initiators()
    sorted_chatters = sorted(stats.items(), key=lambda item: item[1]['messages_count'], reverse=True)
    
    for name, data in sorted_chatters[:args.top_n]:
        print(f"  {name}:")
        print(f"    Messages: {data['messages_count']}")
        print(f"    Avg Response Time: {data['avg_time']}s")
        print(f"    New Dialogues: {initiators.get(name, 0)}")
        
        # top words (showing top 5)
        top_words = list(data['word_stats'].items())[:5]
        if top_words:
            words_str = ", ".join([f"{w}: {c}" for w, c in top_words])
            print(f"    Top Words: {words_str}")
            
        # top emojis (showing top 5)
        top_emojis = list(data['emojis'].items())[:5]
        if top_emojis:
            emojis_str = ", ".join([f"{e}: {c}" for e, c in top_emojis])
            print(f"    Top Emojis: {emojis_str}")

    print("\n---------------------------\n")

    print(f"Generating visual for top {args.top_n} users...")
    render_recap(stats, output_path, top_n=args.top_n)

    print("Done!")

if __name__ == "__main__":
    main()
