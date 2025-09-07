"""This module contains configuration settings for the Habr parser application."""

import os
from dotenv import load_dotenv

load_dotenv()

# URL to connect to database
DATABASE_URL = os.getenv("DATABASE_URL")
# URL of the Habr page to scrape articles from
BASE_URL = os.getenv("BASE_URL")
