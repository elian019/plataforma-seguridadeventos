from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ─────────────────────────────────────────
# UBICACION
# ─────────────────────────────────────────
class UbicacionBase(BaseModel):
    direccion: Optional[str] = None
    zona: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    referencia: Optional[str] = None

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionUpdate(UbicacionBase):
    pass

class UbicacionOut(UbicacionBase):
    id_ubicacion: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# EMPRESA_SEGURIDAD
# ─────────────────────────────────────────
class EmpresaBase(BaseModel):
    nombre_empresa: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(EmpresaBase):
    nombre_empresa: Optional[str] = None

class EmpresaOut(EmpresaBase):
    id_empresa: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# CENTRO_MONITOREO
# ─────────────────────────────────────────
class CentroBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    id_empresa: Optional[int] = None

class CentroCreate(CentroBase):
    pass

class CentroUpdate(CentroBase):
    nombre: Optional[str] = None

class CentroOut(CentroBase):
    id_centro: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# DISPOSITIVO
# ─────────────────────────────────────────
class DispositivoBase(BaseModel):
    nombre_dispositivo: str
    tipo_dispositivo: Optional[str] = None
    estado: Optional[str] = None
    id_ubicacion: Optional[int] = None

class DispositivoCreate(DispositivoBase):
    pass

class DispositivoUpdate(DispositivoBase):
    nombre_dispositivo: Optional[str] = None

class DispositivoOut(DispositivoBase):
    id_dispositivo: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# NIVEL_RIESGO
# ─────────────────────────────────────────
class NivelRiesgoBase(BaseModel):
    nivel: str
    puntaje: Optional[int] = None
    descripcion: Optional[str] = None

class NivelRiesgoCreate(NivelRiesgoBase):
    pass

class NivelRiesgoUpdate(NivelRiesgoBase):
    nivel: Optional[str] = None

class NivelRiesgoOut(NivelRiesgoBase):
    id_nivel_riesgo: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# TIPO_EVENTO
# ─────────────────────────────────────────
class TipoEventoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class TipoEventoCreate(TipoEventoBase):
    pass

class TipoEventoUpdate(TipoEventoBase):
    nombre: Optional[str] = None

class TipoEventoOut(TipoEventoBase):
    id_tipo_evento: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# FUENTE_EVENTO
# ─────────────────────────────────────────
class FuenteEventoBase(BaseModel):
    nombre_fuente: str
    tipo_fuente: Optional[str] = None
    descripcion: Optional[str] = None

class FuenteEventoCreate(FuenteEventoBase):
    pass

class FuenteEventoUpdate(FuenteEventoBase):
    nombre_fuente: Optional[str] = None

class FuenteEventoOut(FuenteEventoBase):
    id_fuente_evento: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# EVENTO
# ─────────────────────────────────────────
class EventoBase(BaseModel):
    fecha_hora: Optional[datetime] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None
    id_tipo_evento: Optional[int] = None
    id_dispositivo: Optional[int] = None
    id_nivel_riesgo: Optional[int] = None
    id_centro: Optional[int] = None
    id_fuente_evento: Optional[int] = None
    id_ubicacion: Optional[int] = None

class EventoCreate(EventoBase):
    pass

class EventoUpdate(EventoBase):
    pass

class EventoOut(EventoBase):
    id_evento: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# AUDITORIA
# ─────────────────────────────────────────
class AuditoriaBase(BaseModel):
    fecha_hora: Optional[datetime] = None
    accion: Optional[str] = None
    descripcion: Optional[str] = None
    ip_usuario: Optional[str] = None
    id_usuario: Optional[int] = None
    id_evento: Optional[int] = None

class AuditoriaCreate(AuditoriaBase):
    pass

class AuditoriaOut(AuditoriaBase):
    id_auditoria: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# ROL
# ─────────────────────────────────────────
class RolBase(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    pass

class RolUpdate(RolBase):
    nombre_rol: Optional[str] = None

class RolOut(RolBase):
    id_rol: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# PERMISO
# ─────────────────────────────────────────
class PermisoBase(BaseModel):
    nombre_permiso: str
    descripcion: Optional[str] = None

class PermisoCreate(PermisoBase):
    pass

class PermisoUpdate(PermisoBase):
    nombre_permiso: Optional[str] = None

class PermisoOut(PermisoBase):
    id_permiso: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# ROL_PERMISO
# ─────────────────────────────────────────
class RolPermisoBase(BaseModel):
    id_rol: int
    id_permiso: int

class RolPermisoCreate(RolPermisoBase):
    pass

class RolPermisoOut(RolPermisoBase):
    id_rol_permiso: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# USUARIO
# ─────────────────────────────────────────
class UsuarioBase(BaseModel):
    nombre: str
    apellido: Optional[str] = None
    correo: str
    estado: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    contrasena: str

class UsuarioUpdate(UsuarioBase):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    contrasena: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id_usuario: int
    fecha_creacion: Optional[datetime] = None
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# USUARIO_ROL
# ─────────────────────────────────────────
class UsuarioRolBase(BaseModel):
    id_usuario: int
    id_rol: int
    id_evento: Optional[int] = None

class UsuarioRolCreate(UsuarioRolBase):
    pass

class UsuarioRolOut(UsuarioRolBase):
    id_usuario_rol: int
    class Config:
        from_attributes = True
