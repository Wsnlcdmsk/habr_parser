"""This module contains routes for function's that's connected to the user."""
from fastapi import APIRouter


router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me")
async def read_users_me():
    """This function helps user to get information about him/her."""
    pass
