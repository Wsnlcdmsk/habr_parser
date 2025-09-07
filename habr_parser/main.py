"""This module is the main entry point for the Habr parser application."""

from habr_parser.scraper import get_daily_articles, fetch_habr_page
from habr_parser.config import BASE_URL


def main():
    """Main function to run the Habr parser application"""
    page_content = fetch_habr_page(BASE_URL)
    get_daily_articles(page_content)


if __name__ == "__main__":
    main()
