from users.schemas import UserSchema
from auth import utils as auth_utils
from pydantic import BaseModel
from fastapi import (
    APIRouter,
    Depends,
    Form,  # for Form required package python-multipart
    HTTPException, status
)
from typing import Annotated, Any
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
# from fastapi.security import HTTPBearer
from jwt import InvalidTokenError
from datetime import datetime, timezone


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter()

# http_bearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/jwt/login/")


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


def get_current_user(
        payload: Annotated[dict, Depends(get_current_token_payload)]
) -> UserSchema:
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


@router.get("/users/me")
def auth_user_check_self_info(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user: Annotated[UserSchema, Depends(get_current_active_user)]
) -> dict:
    iat = payload["iat"]
    logged_at = datetime.fromtimestamp(iat, tz=timezone.utc)
    dt_local = logged_at.astimezone()  # convert to local timezone
    human_readable_logged_at = dt_local.strftime("%d %b %Y, %H:%M:%S %z") + " UTC"
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": human_readable_logged_at
    }
