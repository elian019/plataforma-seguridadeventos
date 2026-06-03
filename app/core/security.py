# app/core/security.py
import bcrypt


def hash_password(password: str) -> str:
    password_bytes = password.encode()
    if len(password_bytes) > 72:
        raise ValueError("La contraseña no puede superar 72 bytes")
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except (TypeError, ValueError):
        return False
