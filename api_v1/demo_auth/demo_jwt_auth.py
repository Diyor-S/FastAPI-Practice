from users.schemas import UserSchema, TokenInfo
from fastapi import (
    APIRouter,
    Depends,
)
from typing import Annotated

from datetime import datetime, timezone
from api_v1.demo_auth.helpers import (
    create_access_token,
    create_refresh_token,
)
from api_v1.demo_auth.user_related_helpers import (
    http_bearer,
    validate_auth_user,
    get_current_token_payload,
    get_current_active_user,
)

router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(user: Annotated[UserSchema, Depends(validate_auth_user)]) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
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
