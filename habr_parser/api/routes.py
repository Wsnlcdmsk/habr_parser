"""This module contains routes of API."""

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from habr_parser.api.schemas import ArticleCreate, ArticleRead
from habr_parser.db import crud
from habr_parser.db.database import get_session
from habr_parser.services  import article
from habr_parser.services import recommender


router = APIRouter(prefix="/articles")

@router.get("/", response_model=list[ArticleRead])
async def read_all_articles(session: AsyncSession = Depends(get_session)) -> Sequence[ArticleRead]:
    """Retrieve all articles from the database."""

    return await crud.read_all_articles(session)


@router.get("/{article_id}", response_model=ArticleRead)
async def read_article_by_id(article_id: int,
session: AsyncSession = Depends(get_session)) -> ArticleRead:
    """Retrieve articles that belong to a given tag/hub."""

    return await crud.read_article(session, article_id)


@router.get("/tag/{tag_name}", response_model=list[ArticleRead])
async def filter_articles_by_tag(
    tag_name: str,
    session: AsyncSession = Depends(get_session)
) -> Sequence[ArticleRead]:
    """Get articles that contain given hub/tag."""

    return await article.filter_articles_by_tag(session, tag_name)


@router.get("/views/{min_views}", response_model=list[ArticleRead])
async def filter_articles_by_views(
    min_views: int,
    session: AsyncSession = Depends(get_session)
) -> Sequence[ArticleRead]:
    """Get articles with views >= min_views."""

    return await article.filter_articles_by_views(session, min_views)


@router.get("/recommendation/{article_id}", response_model=list[ArticleRead])
async def filter_articles_by_recommendation(
    article_id: int,
    session: AsyncSession = Depends(get_session)
) -> Sequence[ArticleRead]:
    """Recommend similar articles based on embeddings of the given article."""

    return await recommender.recommend_articles(session, article_id)


@router.delete("/{article_id}", response_model=ArticleRead)
async def delete_article(article_id: int, session: AsyncSession = Depends(get_session)):
    """Delete an article by its ID and return deleted article."""
    article_in_db = await crud.read_article(session, article_id)
    if not article_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    await crud.delete_article(session, article_id)
    return article_in_db



@router.post("/", response_model=ArticleRead)
async def add_article(article_in: ArticleCreate,
session: AsyncSession = Depends(get_session)) -> ArticleRead:
    """Add a new article to the database."""

    return await crud.save_article(session, article_in)


@router.put("/{article_id}", response_model=ArticleRead)
async def update_article(article_id: int, article_update: ArticleCreate,
session: AsyncSession = Depends(get_session)) -> ArticleRead:
    """Update an existing article by its ID."""

    db_article = await crud.read_article(session, article_id)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return await crud.update_article(session, article_id, article_update)
