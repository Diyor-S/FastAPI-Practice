from fastapi import Depends
from fastapi_users.authentication.strategy.db import DatabaseStrategy

from core.config import settings
from api.dependencies import get_access_token_db

from typing import Annotated, TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import AccessToken
    from fastapi_users.authentication.strategy.db import AccessTokenDatabase


def get_database_strategy(
    access_tokens_db: Annotated["AccessTokenDatabase[AccessToken]", Depends(get_access_token_db)],
) -> DatabaseStrategy:
    return DatabaseStrategy(access_tokens_db, lifetime_seconds=settings.access_token.lifetime_seconds)
