"""This module contains documents's models for user."""
from beanie  import Document


class User(Document):
    """This class represents user."""
    username: str
    email: str | None = None
    hashed_password: str

    class Settings:
        """Config user collection"""
        name = "users"
        use_state_management = True

    class Config:
        """Config example to openAPI"""
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
            }
        }
