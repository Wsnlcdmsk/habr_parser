"""This module contains function to filter articles."""

from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from habr_parser.db import models


async def filter_articles_by_tag(
    session: AsyncSession, tag_name: str
) -> Sequence[models.Article]:
    """Return all articles that have given hub/tag."""

    stmt = (
        select(models.Article)
        .join(models.Article.articles_hubs)
        .join(models.ArticleHub.hub)
        .where(models.Hub.name == tag_name)
    )
    
    result = await session.execute(stmt)
    return result.scalars().all()


async def filter_articles_by_views(
    session: AsyncSession, min_views: int
) -> Sequence[models.Article]:
    """Return all articles with views >= min_views."""

    stmt = select(models.Article).where(models.Article.views >= min_views)
    result = await session.execute(stmt)
    return result.scalars().all()


async def filter_articles_by_tops(session: AsyncSession) -> Sequence[models.Article]:
    """Return all articles with is_top eqaul to True."""

    stmt = select(models.Article).where(models.Article.is_top)
    result = await session.execute(stmt)
    return result.scalars().all()
