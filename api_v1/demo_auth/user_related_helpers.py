from fastapi import (
    Depends,
    HTTPException,
    status,
)

from users.schemas import UserSchema, users_db

from api_v1.demo_auth.helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from api_v1.demo_auth.validation import get_current_token_payload

from typing import Annotated


def get_current_user(
        payload: Annotated[dict, Depends(get_current_token_payload)]
) -> UserSchema:
    token_type = payload[TOKEN_TYPE_FIELD]
    if token_type != ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type, got {token_type}, expected {ACCESS_TOKEN_TYPE}"
        )

    username = payload["username"]
    if username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token (user not found)"
        )
    return users_db[username]


def get_current_active_user(user: Annotated[UserSchema, Depends(get_current_user)]) -> UserSchema:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user


def get_current_user_for_refresh(
        payload: Annotated[dict, Depends(get_current_token_payload)]
) -> UserSchema:
    token_type = payload[TOKEN_TYPE_FIELD]
    if token_type != REFRESH_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type, got {token_type}, expected {REFRESH_TOKEN_TYPE}"
        )

    username = payload["username"]
    if username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token (user not found)"
        )
    return users_db[username]
