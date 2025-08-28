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


def validate_token_type(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        token_type: str,
):
    current_token_type = payload[TOKEN_TYPE_FIELD]
    if current_token_type != token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token type, got {current_token_type}, expected {token_type}"
        )
    return True


def get_user_by_sub(payload: Annotated[dict, Depends(get_current_token_payload)]) -> UserSchema:
    username = payload["sub"]
    if username not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token (user not found)"
        )
    return users_db[username]


def get_current_user_from_token_type(token_type: str):
    def get_current_user_from_token(
        payload: Annotated[dict, Depends(get_current_token_payload)]
    ):
        validate_token_type(payload, token_type)
        return get_user_by_sub(payload)
    return get_current_user_from_token


# We can now pass this get_current_user to Depends it would call it.
get_current_user = get_current_user_from_token_type(ACCESS_TOKEN_TYPE)

# No need for this anymore: since it is solved with the higher order versatile function
# def get_current_user(
#         payload: Annotated[dict, Depends(get_current_token_payload)]
# ) -> UserSchema:
#     validate_token_type(payload, payload[ACCESS_TOKEN_TYPE])
#     return get_user_by_sub(payload)


def get_current_active_user(user: Annotated[UserSchema, Depends(get_current_user)]) -> UserSchema:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user


class UserGetterFromToken:
    def __init__(self, token_type):
        self.token_type = token_type

    def __call__(
        self,
        payload: Annotated[dict, Depends(get_current_token_payload)]
    ):
        validate_token_type(payload, token_type=self.token_type)
        return get_user_by_sub(payload)


get_current_user_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)

# No need for this anymore: since the above class implements method call and gets the user.
# def get_current_user_for_refresh(
#         payload: Annotated[dict, Depends(get_current_token_payload)]
# ) -> UserSchema:
#     validate_token_type(payload, payload[REFRESH_TOKEN_TYPE])
#     return get_user_by_sub(payload)



