import time
from datetime import datetime

def make_review(text: str, rating: int, source: str) -> dict:
    """Create a review dictionary with the given text, rating, and source."""
    return {
        'text': text.strip(),
        'rating': rating,
        'source': source(),
        'timestamp': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    }