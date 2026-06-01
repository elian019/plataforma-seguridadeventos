from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

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

from app.core.security import hash_password

router = APIRouter()


# ══════════════════════════════════════════════════════
# UBICACION
# ══════════════════════════════════════════════════════
@router.post("/ubicaciones/", response_model=UbicacionOut, status_code=status.HTTP_201_CREATED, tags=["Ubicación"])
def crear_ubicacion(data: UbicacionCreate, db: Session = Depends(get_db)):
    obj = Ubicacion(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/ubicaciones/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Ubicación"])
def eliminar_ubicacion(id: int, db: Session = Depends(get_db)):
    obj = db.query(Ubicacion).filter(Ubicacion.id_ubicacion == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# EMPRESA_SEGURIDAD
# ══════════════════════════════════════════════════════
@router.post("/empresas/", response_model=EmpresaOut, status_code=201, tags=["Empresa Seguridad"])
def crear_empresa(data: EmpresaCreate, db: Session = Depends(get_db)):
    obj = EmpresaSeguridad(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/empresas/{id}", status_code=204, tags=["Empresa Seguridad"])
def eliminar_empresa(id: int, db: Session = Depends(get_db)):
    obj = db.query(EmpresaSeguridad).filter(EmpresaSeguridad.id_empresa == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# CENTRO_MONITOREO
# ══════════════════════════════════════════════════════
@router.post("/centros/", response_model=CentroOut, status_code=201, tags=["Centro Monitoreo"])
def crear_centro(data: CentroCreate, db: Session = Depends(get_db)):
    obj = CentroMonitoreo(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/centros/{id}", status_code=204, tags=["Centro Monitoreo"])
def eliminar_centro(id: int, db: Session = Depends(get_db)):
    obj = db.query(CentroMonitoreo).filter(CentroMonitoreo.id_centro == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Centro no encontrado")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# DISPOSITIVO
# ══════════════════════════════════════════════════════
@router.post("/dispositivos/", response_model=DispositivoOut, status_code=201, tags=["Dispositivo"])
def crear_dispositivo(data: DispositivoCreate, db: Session = Depends(get_db)):
    obj = Dispositivo(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/dispositivos/{id}", status_code=204, tags=["Dispositivo"])
def eliminar_dispositivo(id: int, db: Session = Depends(get_db)):
    obj = db.query(Dispositivo).filter(Dispositivo.id_dispositivo == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# NIVEL_RIESGO
# ══════════════════════════════════════════════════════
@router.post("/niveles-riesgo/", response_model=NivelRiesgoOut, status_code=201, tags=["Nivel Riesgo"])
def crear_nivel_riesgo(data: NivelRiesgoCreate, db: Session = Depends(get_db)):
    obj = NivelRiesgo(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/niveles-riesgo/{id}", status_code=204, tags=["Nivel Riesgo"])
def eliminar_nivel_riesgo(id: int, db: Session = Depends(get_db)):
    obj = db.query(NivelRiesgo).filter(NivelRiesgo.id_nivel_riesgo == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Nivel de riesgo no encontrado")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# TIPO_EVENTO
# ══════════════════════════════════════════════════════
@router.post("/tipos-evento/", response_model=TipoEventoOut, status_code=201, tags=["Tipo Evento"])
def crear_tipo_evento(data: TipoEventoCreate, db: Session = Depends(get_db)):
    obj = TipoEvento(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/tipos-evento/{id}", status_code=204, tags=["Tipo Evento"])
def eliminar_tipo_evento(id: int, db: Session = Depends(get_db)):
    obj = db.query(TipoEvento).filter(TipoEvento.id_tipo_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Tipo de evento no encontrado")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# FUENTE_EVENTO
# ══════════════════════════════════════════════════════
@router.post("/fuentes-evento/", response_model=FuenteEventoOut, status_code=201, tags=["Fuente Evento"])
def crear_fuente_evento(data: FuenteEventoCreate, db: Session = Depends(get_db)):
    obj = FuenteEvento(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/fuentes-evento/{id}", status_code=204, tags=["Fuente Evento"])
def eliminar_fuente_evento(id: int, db: Session = Depends(get_db)):
    obj = db.query(FuenteEvento).filter(FuenteEvento.id_fuente_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Fuente de evento no encontrada")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# EVENTO
# ══════════════════════════════════════════════════════
@router.post("/eventos/", response_model=EventoOut, status_code=201, tags=["Evento"])
def crear_evento(data: EventoCreate, db: Session = Depends(get_db)):
    obj = Evento(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/eventos/{id}", status_code=204, tags=["Evento"])
def eliminar_evento(id: int, db: Session = Depends(get_db)):
    obj = db.query(Evento).filter(Evento.id_evento == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# AUDITORIA
# ══════════════════════════════════════════════════════
@router.post("/auditorias/", response_model=AuditoriaOut, status_code=201, tags=["Auditoría"])
def crear_auditoria(data: AuditoriaCreate, db: Session = Depends(get_db)):
    obj = Auditoria(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# ROL
# ══════════════════════════════════════════════════════
@router.post("/roles/", response_model=RolOut, status_code=201, tags=["Rol"])
def crear_rol(data: RolCreate, db: Session = Depends(get_db)):
    obj = Rol(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/roles/{id}", status_code=204, tags=["Rol"])
def eliminar_rol(id: int, db: Session = Depends(get_db)):
    obj = db.query(Rol).filter(Rol.id_rol == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# PERMISO
# ══════════════════════════════════════════════════════
@router.post("/permisos/", response_model=PermisoOut, status_code=201, tags=["Permiso"])
def crear_permiso(data: PermisoCreate, db: Session = Depends(get_db)):
    obj = Permiso(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/permisos/{id}", status_code=204, tags=["Permiso"])
def eliminar_permiso(id: int, db: Session = Depends(get_db)):
    obj = db.query(Permiso).filter(Permiso.id_permiso == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# ROL_PERMISO
# ══════════════════════════════════════════════════════
@router.post("/roles-permisos/", response_model=RolPermisoOut, status_code=201, tags=["Rol-Permiso"])
def asignar_permiso_a_rol(data: RolPermisoCreate, db: Session = Depends(get_db)):
    obj = RolPermiso(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/roles-permisos/", response_model=List[RolPermisoOut], tags=["Rol-Permiso"])
def listar_roles_permisos(db: Session = Depends(get_db)):
    return db.query(RolPermiso).all()

@router.delete("/roles-permisos/{id}", status_code=204, tags=["Rol-Permiso"])
def eliminar_rol_permiso(id: int, db: Session = Depends(get_db)):
    obj = db.query(RolPermiso).filter(RolPermiso.id_rol_permiso == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Relación Rol-Permiso no encontrada")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# USUARIO
# ══════════════════════════════════════════════════════
@router.post("/usuarios/", response_model=UsuarioOut, status_code=201, tags=["Usuario"])
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    data_dict = data.model_dump()
    data_dict["contrasena"] = hash_password(data_dict["contrasena"])
    obj = Usuario(**data_dict)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

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
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/usuarios/{id}", status_code=204, tags=["Usuario"])
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    obj = db.query(Usuario).filter(Usuario.id_usuario == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(obj); db.commit()


# ══════════════════════════════════════════════════════
# USUARIO_ROL
# ══════════════════════════════════════════════════════
@router.post("/usuarios-roles/", response_model=UsuarioRolOut, status_code=201, tags=["Usuario-Rol"])
def asignar_rol_a_usuario(data: UsuarioRolCreate, db: Session = Depends(get_db)):
    obj = UsuarioRol(**data.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/usuarios-roles/", response_model=List[UsuarioRolOut], tags=["Usuario-Rol"])
def listar_usuarios_roles(db: Session = Depends(get_db)):
    return db.query(UsuarioRol).all()

@router.delete("/usuarios-roles/{id}", status_code=204, tags=["Usuario-Rol"])
def eliminar_usuario_rol(id: int, db: Session = Depends(get_db)):
    obj = db.query(UsuarioRol).filter(UsuarioRol.id_usuario_rol == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Relación Usuario-Rol no encontrada")
    db.delete(obj); db.commit()
