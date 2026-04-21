import time
from datetime import datetime

def make_review(text: str, rating: int, source: str) -> dict:
    """Create a review dictionary with the given text, rating, and source."""
    return {
        'text': text.strip(),
        'rating': rating,
        'source': source,
        'date': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
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
    default_package = f"com.{name_lower.replace(' ', '')}"
    return APP_PACKAGES.get(name_lower, default_package)

def fetch_reviews(app_name: str, source: str = "Google Play", max_reviews: int = 21) -> list:
    from google_play_scraper import reviews, Sort

    package_id = get_package_id(app_name)
    print(f"Fetching reviews for '{app_name}' (package: {package_id}) from {source}...")

    try:
        results, _ = reviews(
            package_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=max_reviews
        )

        cleaned = [
            make_review(r['content'], r.get('score', 1), "Google Play")
            for r in filter(lambda item: item.get('content', '').strip(), results)
        ]

        unique = list({review['text'][:80]: review for review in cleaned}.values())

        messages = [
            f"No reviews found for '{app_name}' on {source}.",
            f"Fetched {len(unique)} unique reviews for '{app_name}' from {source}.",
        ]
        print(messages[bool(unique)])

        time.sleep(5)

        return unique[:max_reviews]
    
    except Exception as e:
        print(f"Error fetching reviews for '{app_name}' from {source}: {e}")
        return []