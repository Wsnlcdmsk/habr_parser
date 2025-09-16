"""This module contains functions for scraping and processing articles from Habr."""

import json
import requests
from bs4 import BeautifulSoup

from habr_parser.services import processor


def fetch_habr_page(url: str) -> str:
    """Fetches HTML page from Habr by URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_articles(page_content: str) -> list[dict]:
    """Parses raw article data from HTML (without cleaning)."""
    soup = BeautifulSoup(page_content, "lxml")
    articles = soup.select("article.tm-articles-list__item")

    results = []
    for art in articles:
        title_tag = art.select_one("a[data-article-link='true']")
        votes_tag = art.select_one(".tm-votes-meter__value")
        author_tag = art.select_one(".tm-user-info__username")
        time_tag = art.select_one("time")
        views_tag = art.select_one(".tm-icon-counter__value")
        comments_tag = art.select_one(".tm-article-comments-counter-link__value")
        hubs_tags = art.select(".tm-publication-hub__link span")

        results.append({
            "title": title_tag.get_text(strip=True) if title_tag else "",
            "url": "https://habr.com" + title_tag["href"] if title_tag else "",
            "votes": votes_tag.get_text(strip=True) if votes_tag else "0",
            "author": author_tag.get_text(strip=True) if author_tag else None,
            "published": time_tag.get("datetime") if time_tag else None,
            "views": views_tag.get("title") if views_tag else "0",
            "comments": comments_tag.get_text(strip=True) if comments_tag else "0",
            "hubs": [
                hub.get_text(strip=True)
                for hub in hubs_tags if hub.get_text(strip=True) != "*"
            ] if hubs_tags else []
        })

    return results


def get_daily_articles(url: str) -> list[dict]:
    """
    Fetches, parses, processes, and saves daily articles from Habr.
    Full pipeline:
    1. Fetch HTML
    2. Extract raw articles
    3. Clean & normalize with processor
    4. Save to JSON
    """
    page_content = fetch_habr_page(url)
    raw_articles = parse_articles(page_content)
    processed_articles = processor.process_articles(raw_articles)

    with open("data/articles.json", "w", encoding="utf-8") as f:
        json.dump(processed_articles, f, ensure_ascii=False, indent=2)

    return processed_articles
