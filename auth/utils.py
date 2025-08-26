import jwt  # PyJWT library: to create (encode) access tokens
# and verify/extract data from them by decoding.
import bcrypt   # bcrypt library: to hash passwords securely
# and validate user-provided passwords against stored hashes.
from core.config import settings  # custom settings data to store config data.
from datetime import datetime, timedelta, UTC


# This encode_jwt returns an access token.
def encode_jwt(
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    modified_payload = payload.copy()
    # now_depr = datetime.utcnow()
    now_main = datetime.now(UTC).replace(tzinfo=None)

    if expire_timedelta:
        expires = int((now_main + expire_timedelta).timestamp())
    else:
        expires = int((now_main + timedelta(minutes=expire_minutes)).timestamp())

    modified_payload.update(
        exp=expires,
        iat=int(now_main.timestamp()),
        # created_at=int(now_depr.timestamp())
    )
    # Alternative:
    # encoded = jwt.encode(
    #     payload, private_key, algorithm=algorithm
    # )
    # return encoded
    return jwt.encode(modified_payload, private_key, algorithm=algorithm)


# This one is used in my case to return the user data fake 'db' dictionary's UserSchema,
# via that access token that the function above returns.
def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    # decoded = jwt.decode(
    #     token, public_key, algorithms=[algorithm]
    # )
    # return decoded
    return jwt.decode(token, public_key, algorithms=[algorithm])


# Receiving the password type str from the user. Then turning into bytes to hash it.
# This hashed password would have been saved to the database.
def hash_password(password: str) -> bytes:
    # Alternatively, could do password_bytes = password.encode() and then pass it in hashpw(password_bytes)
    # The same for salt = bcrypt.gensalt(), then pass fully: hashpw(password_bytes, salt)
    # This one is also an alternative:
    # hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    # return hashed_password
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


# This function accepts the password from the client,
# while the hash_password should come from the database
# Then it compares two of them and tells whether passwords match or not, meaning True or False.
def validate_password(password: str, hashed_password: bytes) -> bool:
    # Alternative:
    # checked_password = bcrypt.checkpw(password.encode(), hashed_password)
    # return checked_password
    return bcrypt.checkpw(password.encode(), hashed_password)


