from core.models import Base
from core.models.mixins import IntIdPkMixin
from core.types import UserIdType
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    @classmethod
    def get_user_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)

