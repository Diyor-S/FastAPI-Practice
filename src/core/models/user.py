from core.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi import Depends


class User(Base, SQLAlchemyBaseUserTable[int]):
    pass

