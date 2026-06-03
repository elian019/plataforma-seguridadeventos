from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.database import get_db
from app.models.models import (
    Ubicacion, EmpresaSeguridad, CentroMonitoreo, Dispositivo,
    NivelRiesgo, TipoEvento, FuenteEvento, Evento,
    Auditoria, Rol, Permiso, RolPermiso, Usuario, UsuarioRol
)
from app.schemas.schemas import (
    UbicacionCreate, UbicacionUpdate, UbicacionOut,
    EmpresaCreate, EmpresaUpdate, EmpresaOut,
    CentroCreate, CentroUpdate, CentroOut,
    DispositivoCreate, DispositivoUpdate, DispositivoOut,
    NivelRiesgoCreate, NivelRiesgoUpdate, NivelRiesgoOut,
    TipoEventoCreate, TipoEventoUpdate, TipoEventoOut,
    FuenteEventoCreate, FuenteEventoUpdate, FuenteEventoOut,
    EventoCreate, EventoUpdate, EventoOut,
    AuditoriaCreate, AuditoriaOut,
    RolCreate, RolUpdate, RolOut,
    PermisoCreate, PermisoUpdate, PermisoOut,
    RolPermisoCreate, RolPermisoOut,
    UsuarioCreate, UsuarioUpdate, UsuarioOut,
    UsuarioRolCreate, UsuarioRolOut,
)

from app.core.security import hash_password, verify_password

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


router = APIRouter(dependencies=[Depends(get_current_user)])


def confirmar_cambios(db: Session, obj=None):
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto de integridad en los datos") from exc

    if obj is not None:
        db.refresh(obj)
    return obj


def guardar_objeto(db: Session, obj):
    db.add(obj)
    return confirmar_cambios(db, obj)


def eliminar_objeto(db: Session, obj) -> None:
    db.delete(obj)
    confirmar_cambios(db)


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


# ══════════════════════════════════════════════════════
# UBICACION
# ══════════════════════════════════════════════════════
@router.post("/ubicaciones/", response_model=UbicacionOut, status_code=status.HTTP_201_CREATED, tags=["Ubicación"])
def crear_ubicacion(data: UbicacionCreate, db: Session = Depends(get_db)):
    obj = Ubicacion(**data.model_dump())
    return guardar_objeto(db, obj)

@router.get("/ubicaciones/", response_model=List[UbicacionOut], tags=["Ubicación"])
def listar_ubicaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Ubicacion).offset(skip).limit(limit).all()

@router.get("/ubicaciones/{id}", response_model=UbicacionOut, tags=["Ubicación"])
def obtener_ubicacion(id: int, db: Session = Depends(get_db)):
    obj = db.query(Ubicacion).filter(Ubicacion.id_ubicacion == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return obj

@router.put("/ubicaciones/{id}", response_model=UbicacionOut, tags=["Ubicación"])
def actualizar_ubicacion(id: int, data: UbicacionUpdate, db: Session = Depends(get_db)):
    obj = db.query(Ubicacion).filter(Ubicacion.id_ubicacion == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/ubicaciones/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Ubicación"])
def eliminar_ubicacion(id: int, db: Session = Depends(get_db)):
    obj = db.query(Ubicacion).filter(Ubicacion.id_ubicacion == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# EMPRESA_SEGURIDAD
# ══════════════════════════════════════════════════════
@router.post("/empresas/", response_model=EmpresaOut, status_code=201, tags=["Empresa Seguridad"])
def crear_empresa(data: EmpresaCreate, db: Session = Depends(get_db)):
    obj = EmpresaSeguridad(**data.model_dump())
    return guardar_objeto(db, obj)

@router.get("/empresas/", response_model=List[EmpresaOut], tags=["Empresa Seguridad"])
def listar_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(EmpresaSeguridad).offset(skip).limit(limit).all()

@router.get("/empresas/{id}", response_model=EmpresaOut, tags=["Empresa Seguridad"])
def obtener_empresa(id: int, db: Session = Depends(get_db)):
    obj = db.query(EmpresaSeguridad).filter(EmpresaSeguridad.id_empresa == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return obj

@router.put("/empresas/{id}", response_model=EmpresaOut, tags=["Empresa Seguridad"])
def actualizar_empresa(id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    obj = db.query(EmpresaSeguridad).filter(EmpresaSeguridad.id_empresa == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/empresas/{id}", status_code=204, tags=["Empresa Seguridad"])
def eliminar_empresa(id: int, db: Session = Depends(get_db)):
    obj = db.query(EmpresaSeguridad).filter(EmpresaSeguridad.id_empresa == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# CENTRO_MONITOREO
# ══════════════════════════════════════════════════════
@router.post("/centros/", response_model=CentroOut, status_code=201, tags=["Centro Monitoreo"])
def crear_centro(data: CentroCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    obj = CentroMonitoreo(**valores)
    return guardar_objeto(db, obj)

@router.get("/centros/", response_model=List[CentroOut], tags=["Centro Monitoreo"])
def listar_centros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(CentroMonitoreo).offset(skip).limit(limit).all()

@router.get("/centros/{id}", response_model=CentroOut, tags=["Centro Monitoreo"])
def obtener_centro(id: int, db: Session = Depends(get_db)):
    obj = db.query(CentroMonitoreo).filter(CentroMonitoreo.id_centro == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    return obj

@router.put("/centros/{id}", response_model=CentroOut, tags=["Centro Monitoreo"])
def actualizar_centro(id: int, data: CentroUpdate, db: Session = Depends(get_db)):
    obj = db.query(CentroMonitoreo).filter(CentroMonitoreo.id_centro == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    valores = data.model_dump(exclude_unset=True)
    validar_referencias(db, valores)
    for k, v in valores.items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/centros/{id}", status_code=204, tags=["Centro Monitoreo"])
def eliminar_centro(id: int, db: Session = Depends(get_db)):
    obj = db.query(CentroMonitoreo).filter(CentroMonitoreo.id_centro == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# DISPOSITIVO
# ══════════════════════════════════════════════════════
@router.post("/dispositivos/", response_model=DispositivoOut, status_code=201, tags=["Dispositivo"])
def crear_dispositivo(data: DispositivoCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    obj = Dispositivo(**valores)
    return guardar_objeto(db, obj)

@router.get("/dispositivos/", response_model=List[DispositivoOut], tags=["Dispositivo"])
def listar_dispositivos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Dispositivo).offset(skip).limit(limit).all()

@router.get("/dispositivos/{id}", response_model=DispositivoOut, tags=["Dispositivo"])
def obtener_dispositivo(id: int, db: Session = Depends(get_db)):
    obj = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return obj

@router.put("/dispositivos/{id}", response_model=DispositivoOut, tags=["Dispositivo"])
def actualizar_dispositivo(id: int, data: DispositivoUpdate, db: Session = Depends(get_db)):
    obj = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    valores = data.model_dump(exclude_unset=True)
    validar_referencias(db, valores)
    for k, v in valores.items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/dispositivos/{id}", status_code=204, tags=["Dispositivo"])
def eliminar_dispositivo(id: int, db: Session = Depends(get_db)):
    obj = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# NIVEL_RIESGO
# ══════════════════════════════════════════════════════
@router.post("/niveles-riesgo/", response_model=NivelRiesgoOut, status_code=201, tags=["Nivel Riesgo"])
def crear_nivel_riesgo(data: NivelRiesgoCreate, db: Session = Depends(get_db)):
    obj = NivelRiesgo(**data.model_dump())
    return guardar_objeto(db, obj)

@router.get("/niveles-riesgo/", response_model=List[NivelRiesgoOut], tags=["Nivel Riesgo"])
def listar_niveles_riesgo(db: Session = Depends(get_db)):
    return db.query(NivelRiesgo).all()

@router.get("/niveles-riesgo/{id}", response_model=NivelRiesgoOut, tags=["Nivel Riesgo"])
def obtener_nivel_riesgo(id: int, db: Session = Depends(get_db)):
    obj = db.query(NivelRiesgo).filter(NivelRiesgo.id_nivel_riesgo == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Nivel de riesgo no encontrado")
    return obj

@router.put("/niveles-riesgo/{id}", response_model=NivelRiesgoOut, tags=["Nivel Riesgo"])
def actualizar_nivel_riesgo(id: int, data: NivelRiesgoUpdate, db: Session = Depends(get_db)):
    obj = db.query(NivelRiesgo).filter(NivelRiesgo.id_nivel_riesgo == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Nivel de riesgo no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/niveles-riesgo/{id}", status_code=204, tags=["Nivel Riesgo"])
def eliminar_nivel_riesgo(id: int, db: Session = Depends(get_db)):
    obj = db.query(NivelRiesgo).filter(NivelRiesgo.id_nivel_riesgo == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Nivel de riesgo no encontrado")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# TIPO_EVENTO
# ══════════════════════════════════════════════════════
@router.post("/tipos-evento/", response_model=TipoEventoOut, status_code=201, tags=["Tipo Evento"])
def crear_tipo_evento(data: TipoEventoCreate, db: Session = Depends(get_db)):
    obj = TipoEvento(**data.model_dump())
    return guardar_objeto(db, obj)

@router.get("/tipos-evento/", response_model=List[TipoEventoOut], tags=["Tipo Evento"])
def listar_tipos_evento(db: Session = Depends(get_db)):
    return db.query(TipoEvento).all()

@router.get("/tipos-evento/{id}", response_model=TipoEventoOut, tags=["Tipo Evento"])
def obtener_tipo_evento(id: int, db: Session = Depends(get_db)):
    obj = db.query(TipoEvento).filter(TipoEvento.id_tipo_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Tipo de evento no encontrado")
    return obj

@router.put("/tipos-evento/{id}", response_model=TipoEventoOut, tags=["Tipo Evento"])
def actualizar_tipo_evento(id: int, data: TipoEventoUpdate, db: Session = Depends(get_db)):
    obj = db.query(TipoEvento).filter(TipoEvento.id_tipo_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Tipo de evento no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/tipos-evento/{id}", status_code=204, tags=["Tipo Evento"])
def eliminar_tipo_evento(id: int, db: Session = Depends(get_db)):
    obj = db.query(TipoEvento).filter(TipoEvento.id_tipo_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Tipo de evento no encontrado")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# FUENTE_EVENTO
# ══════════════════════════════════════════════════════
@router.post("/fuentes-evento/", response_model=FuenteEventoOut, status_code=201, tags=["Fuente Evento"])
def crear_fuente_evento(data: FuenteEventoCreate, db: Session = Depends(get_db)):
    obj = FuenteEvento(**data.model_dump())
    return guardar_objeto(db, obj)

@router.get("/fuentes-evento/", response_model=List[FuenteEventoOut], tags=["Fuente Evento"])
def listar_fuentes_evento(db: Session = Depends(get_db)):
    return db.query(FuenteEvento).all()

@router.get("/fuentes-evento/{id}", response_model=FuenteEventoOut, tags=["Fuente Evento"])
def obtener_fuente_evento(id: int, db: Session = Depends(get_db)):
    obj = db.query(FuenteEvento).filter(FuenteEvento.id_fuente_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Fuente de evento no encontrada")
    return obj

@router.put("/fuentes-evento/{id}", response_model=FuenteEventoOut, tags=["Fuente Evento"])
def actualizar_fuente_evento(id: int, data: FuenteEventoUpdate, db: Session = Depends(get_db)):
    obj = db.query(FuenteEvento).filter(FuenteEvento.id_fuente_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Fuente de evento no encontrada")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/fuentes-evento/{id}", status_code=204, tags=["Fuente Evento"])
def eliminar_fuente_evento(id: int, db: Session = Depends(get_db)):
    obj = db.query(FuenteEvento).filter(FuenteEvento.id_fuente_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Fuente de evento no encontrada")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# EVENTO
# ══════════════════════════════════════════════════════
@router.post("/eventos/", response_model=EventoOut, status_code=201, tags=["Evento"])
def crear_evento(data: EventoCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    obj = Evento(**valores)
    return guardar_objeto(db, obj)

@router.get("/eventos/", response_model=List[EventoOut], tags=["Evento"])
def listar_eventos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Evento).offset(skip).limit(limit).all()

@router.get("/eventos/{id}", response_model=EventoOut, tags=["Evento"])
def obtener_evento(id: int, db: Session = Depends(get_db)):
    obj = db.query(Evento).filter(Evento.id_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return obj

@router.put("/eventos/{id}", response_model=EventoOut, tags=["Evento"])
def actualizar_evento(id: int, data: EventoUpdate, db: Session = Depends(get_db)):
    obj = db.query(Evento).filter(Evento.id_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    valores = data.model_dump(exclude_unset=True)
    validar_referencias(db, valores)
    for k, v in valores.items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/eventos/{id}", status_code=204, tags=["Evento"])
def eliminar_evento(id: int, db: Session = Depends(get_db)):
    obj = db.query(Evento).filter(Evento.id_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# AUDITORIA
# ══════════════════════════════════════════════════════
@router.post("/auditorias/", response_model=AuditoriaOut, status_code=201, tags=["Auditoría"])
def crear_auditoria(data: AuditoriaCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    obj = Auditoria(**valores)
    return guardar_objeto(db, obj)

@router.get("/auditorias/", response_model=List[AuditoriaOut], tags=["Auditoría"])
def listar_auditorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Auditoria).offset(skip).limit(limit).all()

@router.get("/auditorias/{id}", response_model=AuditoriaOut, tags=["Auditoría"])
def obtener_auditoria(id: int, db: Session = Depends(get_db)):
    obj = db.query(Auditoria).filter(Auditoria.id_auditoria == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Auditoría no encontrada")
    return obj

@router.delete("/auditorias/{id}", status_code=204, tags=["Auditoría"])
def eliminar_auditoria(id: int, db: Session = Depends(get_db)):
    obj = db.query(Auditoria).filter(Auditoria.id_auditoria == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Auditoría no encontrada")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# ROL
# ══════════════════════════════════════════════════════
@router.post("/roles/", response_model=RolOut, status_code=201, tags=["Rol"])
def crear_rol(data: RolCreate, db: Session = Depends(get_db)):
    obj = Rol(**data.model_dump())
    return guardar_objeto(db, obj)

@router.get("/roles/", response_model=List[RolOut], tags=["Rol"])
def listar_roles(db: Session = Depends(get_db)):
    return db.query(Rol).all()

@router.get("/roles/{id}", response_model=RolOut, tags=["Rol"])
def obtener_rol(id: int, db: Session = Depends(get_db)):
    obj = db.query(Rol).filter(Rol.id_rol == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return obj

@router.put("/roles/{id}", response_model=RolOut, tags=["Rol"])
def actualizar_rol(id: int, data: RolUpdate, db: Session = Depends(get_db)):
    obj = db.query(Rol).filter(Rol.id_rol == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/roles/{id}", status_code=204, tags=["Rol"])
def eliminar_rol(id: int, db: Session = Depends(get_db)):
    obj = db.query(Rol).filter(Rol.id_rol == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# PERMISO
# ══════════════════════════════════════════════════════
@router.post("/permisos/", response_model=PermisoOut, status_code=201, tags=["Permiso"])
def crear_permiso(data: PermisoCreate, db: Session = Depends(get_db)):
    obj = Permiso(**data.model_dump())
    return guardar_objeto(db, obj)

@router.get("/permisos/", response_model=List[PermisoOut], tags=["Permiso"])
def listar_permisos(db: Session = Depends(get_db)):
    return db.query(Permiso).all()

@router.get("/permisos/{id}", response_model=PermisoOut, tags=["Permiso"])
def obtener_permiso(id: int, db: Session = Depends(get_db)):
    obj = db.query(Permiso).filter(Permiso.id_permiso == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return obj

@router.put("/permisos/{id}", response_model=PermisoOut, tags=["Permiso"])
def actualizar_permiso(id: int, data: PermisoUpdate, db: Session = Depends(get_db)):
    obj = db.query(Permiso).filter(Permiso.id_permiso == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/permisos/{id}", status_code=204, tags=["Permiso"])
def eliminar_permiso(id: int, db: Session = Depends(get_db)):
    obj = db.query(Permiso).filter(Permiso.id_permiso == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# ROL_PERMISO
# ══════════════════════════════════════════════════════
@router.post("/roles-permisos/", response_model=RolPermisoOut, status_code=201, tags=["Rol-Permiso"])
def asignar_permiso_a_rol(data: RolPermisoCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    validar_relacion_rol_permiso_unica(db, valores["id_rol"], valores["id_permiso"])
    obj = RolPermiso(**valores)
    return guardar_objeto(db, obj)

@router.get("/roles-permisos/", response_model=List[RolPermisoOut], tags=["Rol-Permiso"])
def listar_roles_permisos(db: Session = Depends(get_db)):
    return db.query(RolPermiso).all()

@router.delete("/roles-permisos/{id}", status_code=204, tags=["Rol-Permiso"])
def eliminar_rol_permiso(id: int, db: Session = Depends(get_db)):
    obj = db.query(RolPermiso).filter(RolPermiso.id_rol_permiso == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Relación Rol-Permiso no encontrada")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# USUARIO
# ══════════════════════════════════════════════════════
@router.post("/usuarios/", response_model=UsuarioOut, status_code=201, tags=["Usuario"])
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    validar_correo_unico(db, data.correo)
    data_dict = data.model_dump()
    data_dict["contrasena"] = hash_password_or_422(data_dict["contrasena"])
    obj = Usuario(**data_dict)
    return guardar_objeto(db, obj)

@router.get("/usuarios/", response_model=List[UsuarioOut], tags=["Usuario"])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Usuario).offset(skip).limit(limit).all()

@router.get("/usuarios/{id}", response_model=UsuarioOut, tags=["Usuario"])
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    obj = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return obj

@router.put("/usuarios/{id}", response_model=UsuarioOut, tags=["Usuario"])
def actualizar_usuario(id: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    obj = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    valores = data.model_dump(exclude_unset=True)
    if "correo" in valores:
        validar_correo_unico(db, valores["correo"], usuario_id=id)
    if "contrasena" in valores:
        valores["contrasena"] = hash_password_or_422(valores["contrasena"])
    for k, v in valores.items():
        setattr(obj, k, v)
    return confirmar_cambios(db, obj)

@router.delete("/usuarios/{id}", status_code=204, tags=["Usuario"])
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    obj = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    eliminar_objeto(db, obj)


# ══════════════════════════════════════════════════════
# USUARIO_ROL
# ══════════════════════════════════════════════════════
@router.post("/usuarios-roles/", response_model=UsuarioRolOut, status_code=201, tags=["Usuario-Rol"])
def asignar_rol_a_usuario(data: UsuarioRolCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    validar_relacion_usuario_rol_unica(
        db,
        valores["id_usuario"],
        valores["id_rol"],
        valores.get("id_evento"),
    )
    obj = UsuarioRol(**valores)
    return guardar_objeto(db, obj)

@router.get("/usuarios-roles/", response_model=List[UsuarioRolOut], tags=["Usuario-Rol"])
def listar_usuarios_roles(db: Session = Depends(get_db)):
    return db.query(UsuarioRol).all()

@router.delete("/usuarios-roles/{id}", status_code=204, tags=["Usuario-Rol"])
def eliminar_usuario_rol(id: int, db: Session = Depends(get_db)):
    obj = db.query(UsuarioRol).filter(UsuarioRol.id_usuario_rol == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Relación Usuario-Rol no encontrada")
    eliminar_objeto(db, obj)
