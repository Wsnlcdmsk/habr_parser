"""This module contains routes for all authification's functions."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.auth import TokenResponse
from src.schemas.user import UserCreate, UserOut
from src.services import user as UserService
from src.services import auth as AuthService
from src.core.security import verify_password


router = APIRouter(prefix = "/auth", tags = ["Authefication"])

@router.post("/login", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    """This function helps to login into the service."""
    user = await UserService.find_user_by_email(form_data.username)
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return await AuthService.create_tokens(str(user.id))


@router.post("/register", response_model= UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate) -> UserOut:
    """This function helps to register in the service."""
    try:
        user = await UserService.register_user(user_data)

        user_dict = user.model_dump()
        user_dict["id"] = str(user.id)
        user_dict.pop("_id", None)

        return UserOut(**user_dict)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc


@router.post("/logout")
async def logout(token: str):
    """This function helps to logout out of the service."""
    await AuthService.logout(token)
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str) -> TokenResponse:
    """This function helps to refresh our connection to the service."""
    try:
        return await AuthService.refresh_access_and_refresh_token(refresh_token)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        ) from exc
