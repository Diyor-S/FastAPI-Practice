from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.models import User
from core.schemas import UserCreate

from typing import Sequence


async def get_users(
    session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
    session: AsyncSession,
    user: UserCreate,
) -> User:
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    return new_user
