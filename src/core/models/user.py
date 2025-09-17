from core.models import Base
from core.models.mixins import IntIdPkMixin
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi import Depends


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):
    pass

