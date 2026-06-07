from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.models import Usuario


security = HTTPBearer(auto_error=False)


def _auth_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )


def _is_first_user_creation(request: Request, db: Session) -> bool:
    path = request.url.path.rstrip("/")
    return (
        request.method == "POST"
        and path.endswith("/usuarios")
        and db.query(Usuario.id_usuario).first() is None
    )


def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
):
    if _is_first_user_creation(request, db):
        return None

    if credentials is None:
        raise _auth_error()

    try:
        payload = decode_access_token(credentials.credentials)
        usuario_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError):
        raise _auth_error()

    usuario = db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()
    if usuario is None:
        raise _auth_error()

    if usuario.estado and usuario.estado.lower() in {"inactivo", "bloqueado", "suspendido"}:
        raise HTTPException(status_code=403, detail="Usuario inactivo o bloqueado")

    return usuario
