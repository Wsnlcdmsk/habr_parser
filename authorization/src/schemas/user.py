"""This module contains pydantic's schemas for user."""
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """This shema helps to create or login user."""
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """This schema helps to show safe user information."""
    id: str
    username: str
    email: EmailStr | None = None

class UserUpdate(BaseModel):
    """Schema for updating user info."""
    username: str | None = None
    email: EmailStr | None = None
