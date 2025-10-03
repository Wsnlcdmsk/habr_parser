"""This module is the main entry point for the Habr parser application."""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from habr_parser.config import BASE_URL, NUM_PAGE, INTERVAL
from habr_parser.api import routes
from habr_parser.services.scraper import get_daily_articles
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown context for FastAPI."""

    async def scraper_loop():
        while True:
            try:
                print("Fetching articles from Habr...")
                await get_daily_articles(BASE_URL, NUM_PAGE)
                print("Done! Sleeping...")
            except Exception as e:
                print(f"Scraper error: {e}")
            await asyncio.sleep(INTERVAL)

    logging.basicConfig()
    logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)
    task = asyncio.create_task(scraper_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Scraper task cancelled.")

app = FastAPI(title="Habr Scraper API", lifespan = lifespan)
app.include_router(routes.router)
