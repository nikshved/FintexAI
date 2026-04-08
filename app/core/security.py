import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings


def create_access_token(user: object):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRES
    )
    payload = {
        "user_id": user.id,
        "user_roles": user.roles,
        "type": "access",
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY_ACCESS, algorithm=settings.ALGORITHM)


def create_refresh_token(user: object):
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRES)
    payload = {
        "user_id": user.id,
        "user_roles": user.roles,
        "type": "refresh",
        "exp": expire,
    }
    return jwt.encode(
        payload, settings.SECRET_KEY_REFRESH, algorithm=settings.ALGORITHM
    )


def create_verify_token(user: object):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.VERIFY_TOKEN_EXPIRES
    )
    payload = {
        "user_id": user.id,
        "user_roles": user.roles,
        "type": "verify",
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY_VERIFY, algorithm=settings.ALGORITHM)


def decode_token(token: str, token_type: str):
    choice_token_type = {
        "access": settings.SECRET_KEY_ACCESS,
        "refresh": settings.SECRET_KEY_REFRESH,
        "verify": settings.SECRET_KEY_VERIFY,
    }
    return jwt.decode(
        token, choice_token_type.get(token_type), algorithms=[settings.ALGORITHM]
    )
