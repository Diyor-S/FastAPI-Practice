from fastapi import Depends
from core.authentication import UserManager
from api.dependencies import get_user_db

from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_manager(
    user_db: Annotated["SQLAlchemyUserDatabase", Depends(get_user_db)],
):
    yield UserManager(user_db)
