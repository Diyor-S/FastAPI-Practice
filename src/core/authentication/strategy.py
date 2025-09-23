from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

from core.models import AccessToken
from core.config import settings
from typing import Annotated


def get_database_strategy(
    access_token_db: Annotated[AccessTokenDatabase[AccessToken], Depends(AccessToken.get_token_db)],
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=settings.access_token.lifetime_seconds)
