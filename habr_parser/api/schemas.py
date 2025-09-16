"""This module contains schemas fo API."""

from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field


class HubBase(BaseModel):
    """Base schema for Hub (shared fields)."""
    name: str


class HubCreate(HubBase):
    """Schema for creating a Hub (same as HubBase)."""
    pass


class HubRead(HubBase):
    """Schema for reading a Hub (response model)."""
    id: int

    class Config:
        orm_mode = True


class ArticleBase(BaseModel):
    """Base schema for Article (shared fields)."""
    title: str
    url: HttpUrl
    votes: int = 0
    author: str | None = None
    published: datetime | None = None
    views: int = 0
    comments: int = 0


class ArticleCreate(ArticleBase):
    """Schema for creating an Article (includes hubs as plain strings)."""
    hubs: list[str] = Field(default_factory=list)


class ArticleRead(ArticleBase):
    """Schema for reading an Article (response model with hubs relation)."""
    id: int
    hubs: list[HubRead] = Field(default_factory=list)

    class Config:
        orm_mode = True
