"""This module contains logic to work with redis."""
from datetime import timedelta

from src.db.redis import get_redis


async def save_token(token: str, user_id: str, expires_in: timedelta):
    """This function save data to the redis."""
    r = await get_redis()
    await r.setex(
        f"token:{token}", int(expires_in.total_seconds()), user_id
    )

async def is_token_valid(token: str) -> bool:
    """This function check is token exist in dstsbase."""
    r = await get_redis()
    return await r.exists(f"token:{token}") == 1

async def delete_token(token: str):
    """This function delete token from the redis."""
    r = await get_redis()
    await r.delete(f"token:{token}")

async def delete_user_tokens(user_id: str):
    """This function delete all user's tokens from the redis."""
    r = await get_redis()
    keys = await r.keys(f"user:{user_id}:*")
    if keys:
        await r.delete(*keys)
