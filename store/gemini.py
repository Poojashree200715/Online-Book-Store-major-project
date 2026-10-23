import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def get_book_summary(title, author):
    """Ask Gemini for a short summary of a book.

    Returns the summary text, or None if anything goes wrong
    (no API key, network error, quota exceeded, empty answer).
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        logger.warning("GEMINI_API_KEY is not set; skipping summary.")
        return None

    prompt = (
        f'Write a brief, spoiler-free summary (about 80 to 100 words) of the book '
        f'"{title}" by {author}. If you are not sure about this specific book, '
        f"say that you are unsure instead of inventing details. "
        f"Use plain text only, with no markdown or bullet points."
    )

    try:
        response = requests.post(
            API_URL.format(model=settings.GEMINI_MODEL),
            headers={"x-goog-api-key": api_key, "Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30,
        )
        response.raise_for_status()
        parts = response.json()["candidates"][0]["content"]["parts"]
        text = "".join(p.get("text", "") for p in parts if not p.get("thought")).strip()
        return text or None
    except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
        logger.warning("Gemini request failed: %s", exc)
        return None