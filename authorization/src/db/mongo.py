"""This module contains logic to work with mongodb."""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.core.config import settings
from src.models.user import User

client: AsyncIOMotorClient | None = None

async def init_db():
    """This functions open mongodb connection."""
    global client
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    # подключаем Beanie с нашими моделями
    await init_beanie(database=db, document_models=[User])
    print("✅ Beanie initialized and connected to MongoDB")

async def close_db():
    """This function close mongodb connection."""
    if client:
        client.close()
        print("🛑 MongoDB connection closed")
