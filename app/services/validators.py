from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.models import (
    CentroMonitoreo,
    Dispositivo,
    EmpresaSeguridad,
    Evento,
    FuenteEvento,
    NivelRiesgo,
    Permiso,
    Rol,
    RolPermiso,
    TipoEvento,
    Ubicacion,
    Usuario,
    UsuarioRol,
)


def validar_referencias(db: Session, valores: dict) -> None:
    referencias = {
        "id_empresa": (EmpresaSeguridad, EmpresaSeguridad.id_empresa, "Empresa no encontrada"),
        "id_ubicacion": (Ubicacion, Ubicacion.id_ubicacion, "Ubicación no encontrada"),
        "id_tipo_evento": (TipoEvento, TipoEvento.id_tipo_evento, "Tipo de evento no encontrado"),
        "id_dispositivo": (Dispositivo, Dispositivo.id_dispositivo, "Dispositivo no encontrado"),
        "id_nivel_riesgo": (NivelRiesgo, NivelRiesgo.id_nivel_riesgo, "Nivel de riesgo no encontrado"),
        "id_centro": (CentroMonitoreo, CentroMonitoreo.id_centro, "Centro no encontrado"),
        "id_fuente_evento": (FuenteEvento, FuenteEvento.id_fuente_evento, "Fuente de evento no encontrada"),
        "id_usuario": (Usuario, Usuario.id_usuario, "Usuario no encontrado"),
        "id_evento": (Evento, Evento.id_evento, "Evento no encontrado"),
        "id_rol": (Rol, Rol.id_rol, "Rol no encontrado"),
        "id_permiso": (Permiso, Permiso.id_permiso, "Permiso no encontrado"),
    }

    for campo, (modelo, columna, detalle) in referencias.items():
        valor = valores.get(campo)
        if valor is not None and db.query(modelo).filter(columna == valor).first() is None:
            raise HTTPException(status_code=404, detail=detalle)


def validar_correo_unico(db: Session, correo: str, usuario_id: Optional[int] = None) -> None:
    query = db.query(Usuario).filter(Usuario.correo == correo)
    if usuario_id is not None:
        query = query.filter(Usuario.id_usuario != usuario_id)
    if query.first():
        raise HTTPException(status_code=409, detail="El correo ya está registrado")


def validar_relacion_rol_permiso_unica(db: Session, id_rol: int, id_permiso: int) -> None:
    existe = db.query(RolPermiso).filter(
        RolPermiso.id_rol == id_rol,
        RolPermiso.id_permiso == id_permiso,
    ).first()
    if existe:
        raise HTTPException(status_code=409, detail="El rol ya tiene asignado ese permiso")


def validar_relacion_usuario_rol_unica(
    db: Session,
    id_usuario: int,
    id_rol: int,
    id_evento: Optional[int],
) -> None:
    existe = db.query(UsuarioRol).filter(
        UsuarioRol.id_usuario == id_usuario,
        UsuarioRol.id_rol == id_rol,
        UsuarioRol.id_evento == id_evento,
    ).first()
    if existe:
        raise HTTPException(status_code=409, detail="El usuario ya tiene asignado ese rol")


def hash_password_or_422(password: str) -> str:
    try:
        return hash_password(password)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
