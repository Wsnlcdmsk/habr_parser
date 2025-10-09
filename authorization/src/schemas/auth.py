"""This module contains pydantic's schemas for token."""
from pydantic import BaseModel


class TokenData(BaseModel):
    """This class saves token data."""
    user_id: str | None = None


class TokenResponse(BaseModel):
    """This class represents tokens."""
    access_token: str
    refresh_token: str
    token_type: str
