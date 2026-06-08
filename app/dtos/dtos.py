from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ─────────────────────────────────────────
# UBICACION
# ─────────────────────────────────────────
class UbicacionBase(BaseModel):
    direccion: Optional[str] = Field(None, max_length=255)
    zona: Optional[str] = Field(None, max_length=100)
    latitud: Optional[float] = Field(None, ge=-90, le=90)
    longitud: Optional[float] = Field(None, ge=-180, le=180)
    referencia: Optional[str] = Field(None, max_length=255)

class UbicacionCreate(UbicacionBase):
    direccion: str = Field(..., min_length=1, max_length=255)

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
    nombre_empresa: str = Field(..., min_length=1, max_length=255)
    direccion: Optional[str] = Field(None, max_length=255)
    telefono: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None

class EmpresaCreate(EmpresaBase):
    pass

class EmpresaUpdate(EmpresaBase):
    nombre_empresa: Optional[str] = Field(None, min_length=1, max_length=255)

class EmpresaOut(EmpresaBase):
    id_empresa: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# CENTRO_MONITOREO
# ─────────────────────────────────────────
class CentroBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    direccion: Optional[str] = Field(None, max_length=255)
    telefono: Optional[str] = Field(None, max_length=50)
    id_empresa: Optional[int] = Field(None, gt=0)

class CentroCreate(CentroBase):
    pass

class CentroUpdate(CentroBase):
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)

class CentroOut(CentroBase):
    id_centro: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# DISPOSITIVO
# ─────────────────────────────────────────
class DispositivoBase(BaseModel):
    nombre_dispositivo: str = Field(..., min_length=1, max_length=255)
    tipo_dispositivo: Optional[str] = Field(None, max_length=100)
    estado: Optional[str] = Field(None, max_length=50)
    id_ubicacion: Optional[int] = Field(None, gt=0)

class DispositivoCreate(DispositivoBase):
    pass

class DispositivoUpdate(DispositivoBase):
    nombre_dispositivo: Optional[str] = Field(None, min_length=1, max_length=255)

class DispositivoOut(DispositivoBase):
    id_dispositivo: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# NIVEL_RIESGO
# ─────────────────────────────────────────
class NivelRiesgoBase(BaseModel):
    nivel: str = Field(..., min_length=1, max_length=100)
    puntaje: Optional[int] = Field(None, ge=0)
    descripcion: Optional[str] = None

class NivelRiesgoCreate(NivelRiesgoBase):
    pass

class NivelRiesgoUpdate(NivelRiesgoBase):
    nivel: Optional[str] = Field(None, min_length=1, max_length=100)

class NivelRiesgoOut(NivelRiesgoBase):
    id_nivel_riesgo: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# TIPO_EVENTO
# ─────────────────────────────────────────
class TipoEventoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = None

class TipoEventoCreate(TipoEventoBase):
    pass

class TipoEventoUpdate(TipoEventoBase):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)

class TipoEventoOut(TipoEventoBase):
    id_tipo_evento: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# FUENTE_EVENTO
# ─────────────────────────────────────────
class FuenteEventoBase(BaseModel):
    nombre_fuente: str = Field(..., min_length=1, max_length=255)
    tipo_fuente: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None

class FuenteEventoCreate(FuenteEventoBase):
    pass

class FuenteEventoUpdate(FuenteEventoBase):
    nombre_fuente: Optional[str] = Field(None, min_length=1, max_length=255)

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
    estado: Optional[str] = Field(None, max_length=50)
    id_tipo_evento: Optional[int] = Field(None, gt=0)
    id_dispositivo: Optional[int] = Field(None, gt=0)
    id_nivel_riesgo: Optional[int] = Field(None, gt=0)
    id_centro: Optional[int] = Field(None, gt=0)
    id_fuente_evento: Optional[int] = Field(None, gt=0)
    id_ubicacion: Optional[int] = Field(None, gt=0)

class EventoCreate(EventoBase):
    descripcion: str = Field(..., min_length=1)
    estado: str = Field(..., min_length=1, max_length=50)
    id_tipo_evento: int = Field(..., gt=0)
    id_nivel_riesgo: int = Field(..., gt=0)
    id_ubicacion: int = Field(..., gt=0)

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
    accion: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    ip_usuario: Optional[str] = Field(None, max_length=50)
    id_usuario: Optional[int] = Field(None, gt=0)
    id_evento: Optional[int] = Field(None, gt=0)

class AuditoriaCreate(AuditoriaBase):
    accion: str = Field(..., min_length=1, max_length=100)
    id_usuario: int = Field(..., gt=0)

class AuditoriaOut(AuditoriaBase):
    id_auditoria: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# ROL
# ─────────────────────────────────────────
class RolBase(BaseModel):
    nombre_rol: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    pass

class RolUpdate(RolBase):
    nombre_rol: Optional[str] = Field(None, min_length=1, max_length=150)

class RolOut(RolBase):
    id_rol: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# PERMISO
# ─────────────────────────────────────────
class PermisoBase(BaseModel):
    nombre_permiso: str = Field(..., min_length=1, max_length=150)
    descripcion: Optional[str] = None

class PermisoCreate(PermisoBase):
    pass

class PermisoUpdate(PermisoBase):
    nombre_permiso: Optional[str] = Field(None, min_length=1, max_length=150)

class PermisoOut(PermisoBase):
    id_permiso: int
    class Config:
        from_attributes = True


# ─────────────────────────────────────────
# ROL_PERMISO
# ─────────────────────────────────────────
class RolPermisoBase(BaseModel):
    id_rol: int = Field(..., gt=0)
    id_permiso: int = Field(..., gt=0)

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
    nombre: str = Field(..., min_length=1, max_length=150)
    apellido: Optional[str] = Field(None, max_length=150)
    correo: EmailStr
    estado: Optional[str] = Field(None, max_length=50)

class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(..., min_length=8, max_length=72)

class UsuarioUpdate(UsuarioBase):
    nombre: Optional[str] = Field(None, min_length=1, max_length=150)
    correo: Optional[EmailStr] = None
    contrasena: Optional[str] = Field(None, min_length=8, max_length=72)

class UsuarioOut(UsuarioBase):
    id_usuario: int
    fecha_creacion: Optional[datetime] = None
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str = Field(..., min_length=1, max_length=72)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ─────────────────────────────────────────
# USUARIO_ROL
# ─────────────────────────────────────────
class UsuarioRolBase(BaseModel):
    id_usuario: int = Field(..., gt=0)
    id_rol: int = Field(..., gt=0)
    id_evento: Optional[int] = Field(None, gt=0)

class UsuarioRolCreate(UsuarioRolBase):
    pass

class UsuarioRolOut(UsuarioRolBase):
    id_usuario_rol: int
    class Config:
        from_attributes = True


__all__ = [
    "AuditoriaBase",
    "AuditoriaCreate",
    "AuditoriaOut",
    "CentroBase",
    "CentroCreate",
    "CentroOut",
    "CentroUpdate",
    "DispositivoBase",
    "DispositivoCreate",
    "DispositivoOut",
    "DispositivoUpdate",
    "EmpresaBase",
    "EmpresaCreate",
    "EmpresaOut",
    "EmpresaUpdate",
    "EventoBase",
    "EventoCreate",
    "EventoOut",
    "EventoUpdate",
    "FuenteEventoBase",
    "FuenteEventoCreate",
    "FuenteEventoOut",
    "FuenteEventoUpdate",
    "LoginRequest",
    "NivelRiesgoBase",
    "NivelRiesgoCreate",
    "NivelRiesgoOut",
    "NivelRiesgoUpdate",
    "PermisoBase",
    "PermisoCreate",
    "PermisoOut",
    "PermisoUpdate",
    "RolBase",
    "RolCreate",
    "RolOut",
    "RolPermisoBase",
    "RolPermisoCreate",
    "RolPermisoOut",
    "RolUpdate",
    "TipoEventoBase",
    "TipoEventoCreate",
    "TipoEventoOut",
    "TipoEventoUpdate",
    "TokenOut",
    "UbicacionBase",
    "UbicacionCreate",
    "UbicacionOut",
    "UbicacionUpdate",
    "UsuarioBase",
    "UsuarioCreate",
    "UsuarioOut",
    "UsuarioRolBase",
    "UsuarioRolCreate",
    "UsuarioRolOut",
    "UsuarioUpdate",
]
