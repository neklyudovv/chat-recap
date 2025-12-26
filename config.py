from pathlib import Path

# paths


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# analysis settings


# chatters with fewer messages than this will be grouped into "Others" (if logic implemented)


MIN_MESSAGES_THRESHOLD = 5
# minimum word length to be considered in "Most Used Words"


MIN_WORD_LENGTH = 5

# visualization settings


COLORS = [
    "#FF5722", "#405DE6", "#2196F3", "#4CAF50", "#FFC107", 
    "#9C27B0", "#00BCD4", "#FF9800", "#795548", "#607D8B"
]
DEFAULT_FIG_SIZE = (10, 12)
OUTPUT_FILENAME = "chat_recap.png"
