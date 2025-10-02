"""This module contains routes of API."""

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from habr_parser.api.schemas import ArticleCreate, ArticleRead
from habr_parser.api.schemas import HubRead
from habr_parser.db.models import Article
from habr_parser.db import crud
from habr_parser.db.database import get_session
from habr_parser.services  import article
from habr_parser.services import recommender


router = APIRouter(prefix="/articles", tags=["Articles"])

def serialize_article(article: Article) -> ArticleRead:
    return ArticleRead(
        id=article.id,
        title=article.title,
        url=article.url,
        votes=article.votes,
        author=article.author,
        published=article.published,
        views=article.views,
        comments=article.comments,
        is_top=article.is_top,
        hubs=[
            HubRead(id=h.id, name=h.name)
            for h in article.hubs
        ]
    )

@router.get("/", response_model=list[ArticleRead], tags=["Crud"])
async def read_all_articles(session: AsyncSession = Depends(get_session)) -> Sequence[ArticleRead]:
    """Retrieve all articles from the database."""

    articles =  await crud.read_all_articles(session)
    return [serialize_article(a) for a in articles]


@router.get("/top", response_model=list[ArticleRead], tags=["Filters"])
async def filter_articles_by_is_top(
    session: AsyncSession = Depends(get_session)
    ) -> Sequence[ArticleRead]:
    """Get articles thats atribute is_top is equal to True"""
    articles = await article.filter_articles_by_tops(session)
    return [serialize_article(a) for a in articles]


@router.get("/{article_id}", response_model=ArticleRead, tags=["Crud"])
async def read_article_by_id(article_id: int,
session: AsyncSession = Depends(get_session)) -> ArticleRead:
    """Retrieve articles that belong to a given tag/hub."""

    article =  await crud.read_article(session, article_id)
    return serialize_article(article)


@router.get("/tag/{tag_name}", response_model=list[ArticleRead], tags=["Filters"])
async def filter_articles_by_tag(
    tag_name: str,
    session: AsyncSession = Depends(get_session)
) -> Sequence[ArticleRead]:
    """Get articles that contain given hub/tag."""

    articles =  await article.filter_articles_by_tag(session, tag_name)
    return [serialize_article(a) for a in articles]


@router.get("/views/{min_views}", response_model=list[ArticleRead], tags=["Filters"])
async def filter_articles_by_views(
    min_views: int,
    session: AsyncSession = Depends(get_session)
) -> Sequence[ArticleRead]:
    """Get articles with views >= min_views."""

    articles =  await article.filter_articles_by_views(session, min_views)
    return [serialize_article(a) for a in articles]


@router.get("/recommendation/{article_id}", response_model=list[ArticleRead], tags=["Filters"])
async def filter_articles_by_recommendation(
    article_id: int,
    session: AsyncSession = Depends(get_session)
) -> Sequence[ArticleRead]:
    """Recommend similar articles based on embeddings of the given article."""
    articles =  await recommender.recommend_articles(session, article_id)
    return [serialize_article(a) for a in articles]


@router.delete("/{article_id}", response_model=ArticleRead, tags=["Crud"])
async def delete_article(article_id: int, session: AsyncSession = Depends(get_session)):
    """Delete an article by its ID and return deleted article."""
    article_in_db = await crud.read_article(session, article_id)
    if not article_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await crud.delete_article(session, article_id)
    return serialize_article(article_in_db)


@router.post("/", response_model=ArticleRead, tags=["Crud"])
async def add_article(article_in: ArticleCreate,
session: AsyncSession = Depends(get_session)) -> ArticleRead:
    """Add a new article to the database."""

    data = article_in.model_dump()
    if "url" in data and data["url"] is not None:
        data["url"] = str(data["url"])

    saved_article = await crud.save_article(session, data)

    hubs_read = [HubRead(id=-1, name=name) for name in saved_article.get("hubs", [])]

    return ArticleRead(
        id=saved_article.get("id"),
        title=saved_article.get("title"),
        url=saved_article.get("url"),
        votes=saved_article.get("votes"),
        author=saved_article.get("author"),
        published=saved_article.get("published"),
        views=saved_article.get("views"),
        comments=saved_article.get("comments"),
        is_top=saved_article.get("is_top"),
        hubs = hubs_read
    )


@router.put("/{article_id}", response_model=ArticleRead, tags=["Crud"])
async def update_article(article_id: int, article_update: ArticleCreate,
session: AsyncSession = Depends(get_session)) -> ArticleRead:
    """Update an existing article by its ID."""

    db_article = await crud.read_article(session, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    updated_article = await crud.update_article(
        session, article_id,
        article_update.model_dump(exclude_unset=True)
        )
    return serialize_article(updated_article)
