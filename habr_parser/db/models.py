"""This module declare db models."""

from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import CheckConstraint


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class Article(Base):
    """Represents an article scraped from Habr."""

    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(String, nullable=False)
    votes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    author: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    comments: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    hubs: Mapped[list["Hub"]] = relationship(
        back_populates="article",
        cascade= "all, delete orphan"
        )

    __table_args__ = (
        CheckConstraint('votes >= 0', name='votes_non_negative'),
        CheckConstraint('views >= 0', name='views_non_negative'),
        CheckConstraint('comments >= 0', name='comments_non_negative'),
    )


class Hub(Base):
    """Represents a hub (category/tag) associated with an Article."""
    __tablename__ = "hubs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hub_name: Mapped[str] = mapped_column(String, nullable=False)
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))

    article: Mapped[Article] = relationship(back_populates="hubs")
