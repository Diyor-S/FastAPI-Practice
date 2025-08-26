from pydantic import BaseModel, EmailStr, ConfigDict
# from pydantic import Field
from typing import Annotated
from annotated_types import MinLen, MaxLen


class CreateUser(BaseModel):
    # Old method for username:
    # username: str = Field(..., min_length=3, max_length=20)
    # New method for username using Annotated:
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    password: bytes
    email: str | None = None
    is_active: bool = True
