"""This module provide service wich is contain business logic for user."""
from src.models.user import User
from src.schemas.user import UserCreate
from src.repositories import user as UserRepository
from src.core.security import get_password_hash


async def register_user(data: UserCreate) -> User:
    """This functions register user."""
    existing_user = await UserRepository.find_user_by_email(str(data.email))
    if existing_user:
        raise ValueError("User already exists")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=get_password_hash(data.password)
    )

    return await UserRepository.create_user(user)


async def delete_user(user_id: id) -> bool:
    """This function delete user."""
    return await UserRepository.delete_user(user_id)


async def update_user(user_id: str, data: dict) -> User:
    """This function update user."""
    if "password" in data:
        data["hashed_password"] = get_password_hash(data.pop("password"))

    return await UserRepository.update_user(user_id, data)


async def get_all_users() -> list[User]:
    """This function get all existing users."""
    return await UserRepository.find_all_users()


async def find_user_by_id(user_id: str) -> User | None:
    """This fucntions find user by id."""
    return await UserRepository.find_user_by_id(user_id)


async def find_user_by_email(user_email: str) -> User | None:
    """This function find user by email."""
    return await UserRepository.find_user_by_email(user_email)
