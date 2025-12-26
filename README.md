# chat-recap

**Chat Recap** is a comprehensive tool for analyzing chat history export data (e.g., from Telegram). It parses message history to provide detailed insights and statistics about user interactions.

> Built with **Pandas**, **Matplotlib**, and **Pydantic**.

## Table of Contents

- [Features](#features)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [TODO](#todo)

---

## Features

- **Message Volume**: Counts total messages for each participant.
- **Word Analysis**: Identifies the most frequently used words (configurable length).
- **Emoji Analysis**: Counts and ranks the most popular emojis.
- **Response Time**: Calculates the average response time for each user.
- **Active Periods**: Identifies the most active time range (e.g., busiest week).
- **Initiators**: Tracks who starts new conversations most often.
- **Visualizations**: Generates dynamic charts (bar charts, word clouds logic) for top active users.

---

## How It Works

The project reads a JSON file containing chat history. It uses **Pydantic** for robust data validation and cleaning. The analysis logic is decoupled from data loading and visualization, ensuring a modular and maintainable codebase.

1.  **Loader**: Reads JSON, validates structure, and filters for valid messages.
2.  **Analyzer**: Processes messages to compute statistics (word frequency, time gaps, etc.).
3.  **Visualizer**: Uses `matplotlib` to render insights into a recap image.

---

## Project Structure

```
.
- main.py        # Entry point: handles CLI args and orchestrates the flow
- config.py      # Configuration (paths, colors, thresholds)
- src/
    - models.py    # Pydantic models (Message, ChatExport)
    - loader.py    # Data loading and validation logic
    - analyzer.py  # Core analysis logic (ChatAnalyzer class)
    - visual.py    # Visualization logic using matplotlib
- data/          # Input directory for JSON files (e.g., result.json)
- output/        # Output directory for generated images
```

---

## Installation

1.  **Clone the repository** (or download the source code).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
---

## Usage

1.  **Prepare Data**: Export your chat history to JSON (e.g., from Telegram Desktop) and place `result.json` in the `data/` folder.
2.  **Run the script**:
    ```bash
    python main.py
    ```
3.  **Custom Arguments**:
    You can specify input/output paths and the number of top users to display:
    ```bash
    python main.py --input data/my_chat.json --output output/my_recap.png --top_n 3
    ```

---

## Example Output

**Console Output:**
```
Loaded 50 valid messages.
Analyzing data...

--- Metrics ---
Global:
  Total Messages: 50
  Most Active Period: 2023-04-30 to 2023-05-06 (50 msgs)

User Stats:
  Alice:
    Messages: 25
    Avg Response Time: 300.0s
    New Dialogues: 1
    Top Words: reply: 18, example: 14, message: 11
    Top Emojis: 😄: 3, 🎶: 2

  Bob:
    Messages: 25
    Avg Response Time: 312.0s
    New Dialogues: 0
    Top Words: reply: 17, example: 14, message: 12, about: 1
    Top Emojis: 🍕: 2, 🌟: 1, 😄: 1

---------------------------

Generating visual for top 2 users...
Saved visualization to .../output/chat_recap.png
Done!
```

**Generated Image (`chat_recap.png`)**:
- **Messages Count**: Bar chart comparing message volume.
- **Avg Response Time**: Bar chart comparing speed of replies.
- **Most Used Words**: Horizontal bar charts for each user's top words.

---

## TODO

- [ ] Add support for more input formats (Discord).
- [ ] Implement sentiment analysis.
- [ ] Create a web interface for easier interaction.