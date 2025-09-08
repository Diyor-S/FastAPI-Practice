from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.schemas import UserRead, UserCreate
from crud import users
from core.models import User, db_helper

from typing import Annotated, Sequence

router = APIRouter()


@router.get("", response_model=list[UserRead])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> Sequence[User]:
    return await users.get_users(session=session)


@router.post("", response_model=UserRead)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_create: UserCreate,
):
    return await users.create_user(
        session=session,
        user=user_create,
    )
