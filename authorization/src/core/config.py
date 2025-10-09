"""This module contains settings for all project."""
import os
from dotenv import load_dotenv


load_dotenv()

class Settings():
    """This class provide settings to rhe whole project."""
    APP_NAME: str = "authorization-service"
    APP_PORT: int = int(os.getenv("APP_PORT"))

    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DB_NAME: str = "auth_service"

    REDIS_URL: str = os.getenv("REDIS_URL")

    JWT_SECRET: str = os.getenv("SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))


settings = Settings()
