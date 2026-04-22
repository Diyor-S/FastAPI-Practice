from core.authentication import bearer_transport
from fastapi_users.authentication import AuthenticationBackend
from api.dependencies import get_database_strategy

authentication_backend = AuthenticationBackend(
    name="database",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
