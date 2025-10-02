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
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for making tables"""
    __abstract__ = True


class ArticleHub(Base):
    """Represents adjacent table of articles and hubs."""

    __tablename__ = "articles_hubs"
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), primary_key=True)
    hub_id: Mapped[int] = mapped_column(ForeignKey("hubs.id"), primary_key=True)

    article: Mapped["Article"] = relationship(
        back_populates="articles_hubs",
        lazy="selectin"
        )

    hub: Mapped["Hub"] = relationship(
        back_populates="articles_hubs",
        lazy="selectin"
        )


class Article(Base):
    """Represents an article scraped from Habr."""

    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    votes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    author: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    comments: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    articles_hubs: Mapped[list["ArticleHub"]] = relationship(
        back_populates="article",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    is_top: Mapped[bool] = mapped_column(Boolean, nullable=False)

    __table_args__ = (
        CheckConstraint('votes >= 0', name='votes_non_negative'),
        CheckConstraint('views >= 0', name='views_non_negative'),
        CheckConstraint('comments >= 0', name='comments_non_negative'),
    )

    @property
    def hubs(self) -> list["Hub"]:
        return [link.hub for link in self.articles_hubs]


class Hub(Base):
    """Represents a hub (category/tag) associated with an Article."""

    __tablename__ = "hubs"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    articles_hubs: Mapped[list["ArticleHub"]] = relationship(
        back_populates="hub",
        lazy="selectin"
    )

    @property
    def articles(self) -> list["Article"]:
        return [link.article for link in self.articles_hubs]
