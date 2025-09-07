"""This module create db engine."""

from sqlalchemy import create_engine

from habr_parser.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo = True)
