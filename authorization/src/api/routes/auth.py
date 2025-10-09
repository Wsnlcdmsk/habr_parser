"""This module contains routes for all authification's functions."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from src.schemas.auth import Token


router = APIRouter(prefix = "/auth", tags = ["authefication"])

@router.get("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """This function helps to login into the service."""
    pass


@router.post("/register")
async def register(email: EmailStr, username: str, password: str):
    """This function helps to register in the service."""
    pass


@router.get("/logout")
async def logout():
    """This function helps to logout out of the service."""
    pass


@router.post("/refresh")
async def refresh(login: str):
    """This function helps to refresh our connection to the service."""
    pass
