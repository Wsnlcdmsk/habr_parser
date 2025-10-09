"""This module contains crus functions for user collection in the mongodb."""
from src.models.user import User


async def find_all_users() -> list[User]:
    """Find whole users in the collection."""
    return await User.find_all().to_list()


async def find_user_by_id(user_id: str) -> User | None:
    """Find user in the collections by id."""
    return await User.get(user_id)


async def find_user_by_email(user_email: str) -> User | None:
    """Find user in the collections by email."""
    return await User.find_one(User.email == user_email)


async def create_user(user: User) -> User:
    """Create new user in the collection."""
    await user.insert()
    return user


async def update_user(user_id: str, data: dict) -> User | None:
    """Update user in the collection."""
    user = await User.get(user_id)
    if not user:
        return None
    await user.set({**data})
    return user


async def delete_user(user_id: str) -> bool:
    """Delete user from the collection."""
    user = await User.get(user_id)
    if not user:
        return False
    user.delete()
    return True
