"""This module contains crud function of db models"""

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from habr_parser.db.models import Article
from habr_parser.db.models import Hub
from habr_parser.db.models import ArticleHub


async def get_or_create_hub(session: AsyncSession, name: str) -> Hub:
    """Find the hub ot create a new one."""

    result = await session.execute(select(Hub).where(Hub.name == name))
    hub = result.scalar_one_or_none()
    if not hub:
        hub = Hub(name=name)
        session.add(hub)
        await session.flush()
    return hub


async def save_article(session: AsyncSession, article_data: dict) -> dict:
    """Save the articles to the database."""
    hubs_names = article_data.pop("hubs", [])
    article = Article(**article_data)
    session.add(article)
    await session.flush()

    for name in hubs_names:
        hub = await get_or_create_hub(session, name)
        link = ArticleHub(article=article, hub=hub)
        session.add(link)

    await session.commit()

    stmt = select(Article).options(
        selectinload(Article.articles_hubs).selectinload(ArticleHub.hub)
    ).where(Article.id == article.id)

    result = await session.execute(stmt)
    article = result.unique().scalar_one()

    return {
        "id": article.id,
        "title": article.title,
        "url": article.url,
        "votes": article.votes,
        "author": article.author,
        "published": article.published,
        "views": article.views,
        "comments": article.comments,
        "is_top": article.is_top,
        "hubs": [link.hub.name for link in article.articles_hubs]
    }



async def read_article(session: AsyncSession, article_id: int) -> Article | None:
    """Read article from the database."""
    result = await session.get(
        Article, article_id,
        options=[selectinload(Article.articles_hubs).selectinload(ArticleHub.hub)]
    )
    return result

async def update_article(
    session: AsyncSession,
    article_id: int,
    new_data: dict
) -> Article | None:
    """Update article fields and hubs in the database."""
    
    article = await session.get(Article, article_id)
    if not article:
        return None

    normal_fields = {k: v for k, v in new_data.items() if k != "hubs"}
    for key, value in normal_fields.items():
        if key == "url" and hasattr(value, "__str__"):
            value = str(value)

        setattr(article, key, value)

    if "hubs" in new_data:
        hubs_names = new_data["hubs"]

        article.articles_hubs.clear()

        for hub_name in hubs_names:
            hub = await get_or_create_hub(session, hub_name)
            article.articles_hubs.append(ArticleHub(hub=hub))

    await session.commit()
    await session.refresh(article)
    return article

async def delete_article(session: AsyncSession, article_id: int) -> None:
    """Remove article from the database by id."""
    article = await read_article(session, article_id)
    if article:
        await session.delete(article)
        await session.commit()


async def read_all_articles(session: AsyncSession) -> list[Article] | None:
    """Read all article from the database."""
    stmt = select(Article)
    result = await session.execute(stmt)
    return result.scalars().unique()

async def save_articles_to_db(session: AsyncSession, articles: list[dict]) -> list[Article]:
    """Save articles to database."""

    saved_articles = []

    for article in articles:
        try:
            saved = await save_article(session, article)
            saved_articles.append(saved)
        except Exception as e:
            await session.rollback()
            print(f"⚠️ Erorr while saving {article.get('title')}: {e}")

    return saved_articles
