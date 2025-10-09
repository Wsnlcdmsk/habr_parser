"""This module contains pydantic's schemas for user."""
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """This shema helps to create or login user."""
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """This shema helps to show some information about current user."""
    id: str
    email: EmailStr
