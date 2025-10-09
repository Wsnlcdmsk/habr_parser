"""This module contains pydantic's schemas for token."""
from pydantic import BaseModel


class Token(BaseModel):
    """This class reperesents token."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """This class saves token data."""
    username: str | None = None
