"""This module contains documents's models for user."""
from beanie  import Document


class User(Document):
    """This class represents user."""
    username: str
    email: str | None = None
    hashed_password: str
