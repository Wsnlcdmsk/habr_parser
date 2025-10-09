"""This module contains main object of service."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes import auth, user
from src.db.mongo import init_mongodb, close_mongodb
from src.db.redis import init_redis, close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """This function init and close MongoDB and Redis."""
    await init_mongodb()
    await init_redis()
    print("🚀 MongoDB and Redis connected")

    yield

    await close_redis()
    await close_mongodb()
    print("🛑 MongoDB and Redis disconnected")


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user.router)
