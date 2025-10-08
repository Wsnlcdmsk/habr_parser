"""This module contains main object of service."""
from fastapi import FastAPI

from src.api.routes import auth, user


app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
