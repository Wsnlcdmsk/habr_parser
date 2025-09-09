"""This module clean, normalize, and filter article data."""

from __future__ import annotations
from datetime import datetime
from typing import Any


def clean_title(title: str) -> str:
    """Removes extra spaces and special characters in the title."""
    return title.strip().replace("\xa0", " ")


def normalize_url(url: str) -> str:
    """Converts relative links into absolute ones (habr.com)."""
    if url.startswith("/"):
        return f"https://habr.com{url}"
    return url


def parse_published(published_str: str | None) -> datetime | None:
    """Parses ISO datetime string into datetime (or None if invalid)."""
    if not published_str:
        return None
    try:
        return datetime.fromisoformat(published_str.replace("Z", "+00:00"))
    except Exception:
        return None


def safe_int(value: Any, default: int = 0) -> int:
    """Safely converts a value to int, or returns default if it fails."""
    try:
        return int(str(value).replace(" ", ""))
    except (ValueError, TypeError):
        return default


def filter_by_votes(articles: list[dict], min_votes: int = 10) -> list[dict]:
    """Keeps only articles with votes ≥ min_votes."""
    return [a for a in articles if safe_int(a.get("votes", 0)) >= min_votes]


def filter_unique(articles: list[dict]) -> list[dict]:
    """Removes duplicate articles based on their URL."""
    seen = set()
    unique_articles = []
    for a in articles:
        url = a.get("url")
        if url and url not in seen:
            seen.add(url)
            unique_articles.append(a)
    return unique_articles


def mark_top_articles(articles: list[dict], min_views: int = 5000) -> list[dict]:
    """Adds 'is_top' flag for articles with views ≥ min_views."""
    for a in articles:
        a["is_top"] = safe_int(a.get("views", 0)) >= min_views
    return articles


def validate_article(article: dict) -> bool:
    """
    Validates that an article is suitable for saving.
    Requires mandatory fields: title, url.
    Ensures votes are not negative.
    """
    if not article.get("title") or not article.get("url"):
        return False
    if safe_int(article.get("votes", 0)) < 0:
        return False
    return True
