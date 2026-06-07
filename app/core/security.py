# app/core/security.py
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from jwt import InvalidTokenError

from app.core.config import settings


def hash_password(password: str) -> str:
    password_bytes = password.encode()
    if len(password_bytes) > 72:
        raise ValueError("La contrasena no puede superar 72 bytes")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except (TypeError, ValueError):
        return False


def create_access_token(subject: str, extra_claims: dict | None = None) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "type": "access",
        "iat": now,
        "exp": expires_at,
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except InvalidTokenError as exc:
        raise ValueError("Token invalido") from exc

    if payload.get("type") != "access":
        raise ValueError("Tipo de token invalido")

    return payload
