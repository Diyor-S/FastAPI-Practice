from core.models import Base
from core.models.mixins import IntIdPkMixin
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):
    pass
