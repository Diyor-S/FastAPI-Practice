from fastapi import (
    Depends,
    Form,  # for Form required package python-multipart
    HTTPException,
    status,
)

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer  # , HTTPAuthorizationCredentials

from users.schemas import UserSchema, users_db

from auth import utils as auth_utils

from jwt import InvalidTokenError
from typing import Annotated


http_bearer = HTTPBearer(auto_error=False)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login/")


def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
) -> UserSchema:
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    if username not in users_db:
        raise unauthorized_exception
    if not auth_utils.validate_password(
            password=password,
            hashed_password=users_db[username].password
    ):
        raise unauthorized_exception
    if not users_db[username].is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive"
        )

    return users_db[username]


def get_current_token_payload(
        # credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
        token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    # token = credentials.credentials
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    try:
        payload = auth_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error {e}"
        )
    return payload
