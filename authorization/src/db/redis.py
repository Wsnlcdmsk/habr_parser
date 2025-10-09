"""This module contains logic to work with redis."""
import redis.asyncio as redis
from src.core.config import settings

redis_client: redis.Redis | None = None

async def init_redis():
    """This functions open redis connection."""
    global redis_client
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    print("✅ Redis connected")

async def close_redis():
    """This function close redis connection."""
    if redis_client:
        await redis_client.close()
        print("🛑 Redis connection closed")

async def get_redis() -> redis.Redis:
    """Get redis client."""
    if redis_client is None:
        raise RuntimeError("Redis is not initialized")
    return redis_client
