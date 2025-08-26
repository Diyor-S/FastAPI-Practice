from users.schemas import UserSchema
from auth import utils as auth_utils
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from typing import Annotated


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter()

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


def validate_auth_user():
    pass


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(user: Annotated[UserSchema, Depends(validate_auth_user)]) -> TokenInfo:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email
    }
    access_token = auth_utils.encode_jwt(jwt_payload)

    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
    )
