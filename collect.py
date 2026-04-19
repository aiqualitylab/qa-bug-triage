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

APP_PACKAGES = {
    "google maps": "com.google.android.apps.maps",
    "facebook":    "com.facebook.katana",
    "instagram":   "com.instagram.android",
    "whatsapp":    "com.whatsapp",
    "snapchat":    "com.snapchat.android",
    "notion":      "com.notion.android",
    "spotify":     "com.spotify.music",
    "netflix":     "com.netflix.mediaclient",
}

def get_package_id(app_name: str) -> str:
    """Return the package ID for the given app name, or a default format if not found."""
    name_lower = app_name.lower().strip()

    if name_lower in APP_PACKAGES:
        return APP_PACKAGES[name_lower]
    
    return f"com.{name_lower.replace(' ', '')}"