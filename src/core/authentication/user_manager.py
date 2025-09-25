from fastapi_users import BaseUserManager, IntegerIDMixin

from core.config import settings
from core.types import UserIdType
from core.models import User

from typing import TYPE_CHECKING, Optional
import logging

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(f"User %r has registered.", user.id)
