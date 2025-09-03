"""This module contains functions for scraping articles from Habr."""

import requests
from bs4 import BeautifulSoup
import json


def fetch_habr_page(url):
    """This module fetch htm-page by using url"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    responce = requests.get(url, headers=headers)
    responce.raise_for_status()
    return responce.text


def get_daily_articles(page_content):
    """Gets list of articles from the page HTML"""
    
    soup = BeautifulSoup(page_content, "lxml")
    articles = soup.select("article.tm-articles-list__item")

    results = []
    for art in articles:
        title_tag = art.select_one("h2 a")
        votes_tag = art.select_one(".tm-votes-meter__value")
        author_tag = art.select_one(".tm-user-info__username")
        time_tag = art.select_one("time")
        views_tag = art.select_one(".tm-icon-counter__value")
        comments_tag = art.select_one(".tm-article-comments-counter-link__value")
        hubs_tags = art.select(".tm-publication-hub__link span")

        results.append({
            "title": title_tag.get_text(strip=True) if title_tag else None,
            "url": "https://habr.com" + title_tag["href"] if title_tag else None,
            "votes": int(votes_tag.get_text(strip=True).replace("+", "")) if votes_tag else 0,
            "author": author_tag.get_text(strip=True) if author_tag else None,
            "published": time_tag.get("datetime") if time_tag else None,
            "views": int(views_tag.get("title")) if views_tag and views_tag.get("title") else None,
            "comments": int(comments_tag.get_text(strip=True)) if comments_tag else 0,
            "hubs": [hub.get_text(strip=True) for hub in hubs_tags] if hubs_tags else []
        })

    with open("data/articles.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return results
