"""This module recomend articlles for user."""

from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from habr_parser.db import models
from habr_parser.services.processor_recomended import ArticleRecommender


async def recommend_articles(
    session: AsyncSession, article_id: int, top_n: int = 5
) -> Sequence[models.Article]:
    """Recommend similar articles based on embeddings of the given article."""

    stmt = select(models.Article)
    result = await session.execute(stmt)
    articles = result.scalars().all()

    if not articles:
        raise HTTPException(status_code=404, detail="No articles in database")

    article_map = {a.id: idx for idx, a in enumerate(articles)}
    if article_id not in article_map:
        raise HTTPException(status_code=404, detail="Article not found")
    target_idx = article_map[article_id]

    texts = [f"{a.title} {' '.join([h.name for h in a.hubs])}" for a in articles]

    recommender = ArticleRecommender(texts)
    recommendations = recommender.recommend(target_idx, top_n=top_n)

    recommended_indices = [
        texts.index(text) for text, _ in recommendations if text in texts
    ]
    return [articles[i] for i in recommended_indices]
