"""This module contains crud function of db models"""

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from habr_parser.db.models import Article


async def save_article(session: AsyncSession, article_data: dict) -> Article:
    """Add article to the database."""
    article = Article(**article_data)
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return article

async def read_article(session: AsyncSession, article_id: int) -> Article | None:
    """Read article from the database."""
    stmt = select(Article).where(Article.id == article_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def update_article(session: AsyncSession, article_id: int, new_data: dict) -> Article | None:
    """Update article in the database."""
    stmt = (
        update(Article)
        .where(Article.id == article_id)
        .values(**new_data)
        .returning(Article)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.scalar_one_or_none()

async def delete_article(session: AsyncSession, article_id: int) -> None:
    """Remove article from the database by id."""
    stmt = delete(Article).where(Article.id == article_id)
    await session.execute(stmt)
    await session.commit()


async def read_all_articles(session: AsyncSession) -> list[Article] | None:
    """Read all article from the database."""
    stmt = select(Article)
    result = await session.execute(stmt)
    return result
