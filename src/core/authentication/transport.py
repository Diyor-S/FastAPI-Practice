from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(
    # TODO: update transport
    tokenUrl="auth/jwt/login",
)
