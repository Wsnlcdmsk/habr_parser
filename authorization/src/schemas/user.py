"""This module contains pydantic's schemas for user."""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from bson import ObjectId

class UserCreate(BaseModel):
    """This shema helps to create or login user."""
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """This schema helps to show safe user information."""
    id: str = Field(..., alias="_id")
    username: str
    email: EmailStr | None = None

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        from_attributes=True,
    )

class UserUpdate(BaseModel):
    """Schema for updating user info."""
    username: str | None = None
    email: EmailStr | None = None
