"""This module contains configuration settings for the Habr parser application."""

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
BASE_URL = os.getenv("BASE_URL")
NUM_PAGE = int(os.getenv("NUM_PAGE"))
INTERVAL = 24 * 60 * 60
