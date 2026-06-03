from typing import Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.db.database import get_db
from app.models.models import Usuario


security = HTTPBasic(auto_error=False)


def _auth_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Basic"},
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
    credentials: Optional[HTTPBasicCredentials] = Depends(security),
    db: Session = Depends(get_db),
):
    if _is_first_user_creation(request, db):
        return None

    if credentials is None:
        raise _auth_error()

    usuario = db.query(Usuario).filter(Usuario.correo == credentials.username).first()
    if usuario is None or not verify_password(credentials.password, usuario.contrasena):
        raise _auth_error()

    if usuario.estado and usuario.estado.lower() in {"inactivo", "bloqueado", "suspendido"}:
        raise HTTPException(status_code=403, detail="Usuario inactivo o bloqueado")

    return usuario
