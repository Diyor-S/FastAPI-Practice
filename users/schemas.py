from pydantic import BaseModel, EmailStr, ConfigDict
# from pydantic import Field
from typing import Annotated
from annotated_types import MinLen, MaxLen
from auth import utils as auth_utils


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


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


john = UserSchema(
    username="john",
    email="john@example.com",
    password=auth_utils.hash_password("qwerty"),
)

sam = UserSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}
