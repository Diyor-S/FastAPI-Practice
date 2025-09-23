from api.api_v1.authentication import bearer_transport, get_database_strategy
from fastapi_users.authentication import AuthenticationBackend

auth_backend = AuthenticationBackend(
    name="database",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
