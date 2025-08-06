from core.models import Base
from sqlalchemy.orm import Mapped
from typing import ClassVar


class Product(Base):

    __tablename__: ClassVar[str] = "products"

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
