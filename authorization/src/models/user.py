"""This module contains pydantic's models for user."""
from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    """This class represents user."""
    username: str
    email: EmailStr | None = None


class UserInDB(BaseUser):
    """This user represents how user stored in database."""
    hashed_password: str
