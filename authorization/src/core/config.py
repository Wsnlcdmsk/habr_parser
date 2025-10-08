"""This module contains settings for all project."""
import os
from dotenv import load_dotenv


load_dotenv()

class Settings():
    """This class provide settings to rhe whole project."""
    APP_NAME: str = "authorization-service"
    APP_PORT: int = int(os.getenv("APP_PORT"))

    JWT_SECRET: str = os.getenv("SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


settings = Settings()
