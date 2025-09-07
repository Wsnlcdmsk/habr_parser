"""This module contains crud function of db models"""

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from habr_parser.db.models import Article, Hub


def save_article(engine: Engine, article_data: dict):
    """This function add article to the database."""

    with Session(engine) as db:
        article = Article(**article_data)
        db.add(article)
        db.commit()
        db.refresh(article)


def delete_article(engine: Engine, article_data: dict):
    """This function remove article from the database."""

    with Session(engine):
        #TODO

def update_article(engine: Engine, article_data: dict):
    """This function update article in the database."""

    with Session(engine):
        #TODO

def read_article(engine: Engine, article_data: dict):
    """This function read article from the database."""

    with Session(engine):
        #TODO
