"""This module contains routes for functions connected to the user."""
from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.user import UserOut, UserUpdate
from src.core.security import oauth2_scheme, decode_token
from src.services import user as UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
async def read_users_me(token: str = Depends(oauth2_scheme)) -> UserOut:
    """Return info about the current user."""
    token_data = decode_token(token)
    user = await UserService.find_user_by_email(token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/me", response_model=UserOut)
async def update_users_me(user_update: UserUpdate, token: str = Depends(oauth2_scheme)) -> UserOut:
    """Update the current user's data."""
    token_data = decode_token(token)
    user = await UserService.update_user(token_data.user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users_me(token: str = Depends(oauth2_scheme)) -> None:
    """Delete the current user's account."""
    token_data = decode_token(token)
    deleted = await UserService.delete_user(token_data.user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None


@router.get("/", response_model=list[UserOut])
async def list_users(token: str = Depends(oauth2_scheme)) -> list[UserOut]:
    """Return a list of all users (admin use)."""
    users = await UserService.get_all_users()
    return users
