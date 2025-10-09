"""Authentication service for managing login, logout, and token refresh."""
from datetime import timedelta

from src.core.config import settings
from src.core.security import create_access_token, decode_token
from src.repositories import token as TokenRepository


async def create_tokens(user_id: str) -> dict:
    """Create access and refresh token's and save it to the redis."""
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    refresh_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


    await TokenRepository.save_token(
        access_token, user_id, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    await TokenRepository.save_token(
        refresh_token, user_id, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def logout(token: str) -> None:
    """Delete token out of the system (delete out from the system)."""
    await TokenRepository.delete_token(token)


async def refresh_access_and_refresh_token(token: str) -> dict:
    """Check refresh token and gives pair of the new tokens."""
    is_valid = await TokenRepository.is_token_valid(token)
    if not is_valid:
        raise ValueError("Invalid or expired refresh token")

    token_data = decode_token(token)
    user_id = token_data.user_id

    await TokenRepository.delete_token(token)

    return await create_tokens(user_id)
