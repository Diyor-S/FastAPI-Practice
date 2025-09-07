from core.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from core.models import IntIdPkMixin


class User(IntIdPkMixin, Base):
    username: Mapped[str] = mapped_column(unique=True)
