"""
processor_recommender.py
Module for generating article embeddings and finding similar ones
(content-based recommendations).
"""

from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load a pre-trained model for text embeddings
# (all-MiniLM-L6-v2 is lightweight and fast, good for prototyping)
model = SentenceTransformer("all-MiniLM-L6-v2")


class ArticleRecommender:
    """
    Class for building vector representations of articles
    and finding similar articles using embeddings.
    """

    def __init__(self, articles: List[str]):
        """
        Initialize the recommender with a list of articles.

        Args:
            articles (List[str]): list of article texts
                                 (can be title + hubs + content)
        """
        self.articles = articles
        # Precompute embeddings for all articles once during initialization
        self.embeddings = self._encode_articles(articles)

    def _encode_articles(self, articles: List[str]) -> np.ndarray:
        """
        Convert a list of articles into embeddings.

        Args:
            articles (List[str]): list of article texts

        Returns:
            np.ndarray: matrix of embeddings,
                        shape (n_articles, embedding_dim)
        """
        return model.encode(articles, convert_to_numpy=True)

    def recommend(self, article_idx: int, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Recommend similar articles for a given article index.

        Args:
            article_idx (int): index of the article in the list
            top_n (int): number of recommendations to return

        Returns:
            List[Tuple[str, float]]: list of (article text, similarity score)
        """
        # Compute cosine similarity between the target article
        # and all other articles in the corpus
        similarities = cosine_similarity(
            [self.embeddings[article_idx]], self.embeddings
        )[0]

        # Get indices of the most similar articles (excluding itself)
        similar_indices = np.argsort(similarities)[::-1][1 : top_n + 1]

        # Return articles and their similarity scores
        return [(self.articles[i], float(similarities[i])) for i in similar_indices]
