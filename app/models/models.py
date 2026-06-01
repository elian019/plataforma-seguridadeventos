from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Ubicacion(Base):
    __tablename__ = "ubicacion"

    id_ubicacion = Column(Integer, primary_key=True, index=True)
    direccion = Column(String(255))
    zona = Column(String(100))
    latitud = Column(Float)
    longitud = Column(Float)
    referencia = Column(String(255))

    dispositivos = relationship("Dispositivo", back_populates="ubicacion")
    eventos = relationship("Evento", back_populates="ubicacion")


class EmpresaSeguridad(Base):
    __tablename__ = "empresa_seguridad"

    id_empresa = Column(Integer, primary_key=True, index=True)
    nombre_empresa = Column(String(255), nullable=False)
    direccion = Column(String(255))
    telefono = Column(String(50))
    email = Column(String(150))

    centros = relationship("CentroMonitoreo", back_populates="empresa")


class CentroMonitoreo(Base):
    __tablename__ = "centro_monitoreo"

    id_centro = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    direccion = Column(String(255))
    telefono = Column(String(50))
    id_empresa = Column(Integer, ForeignKey("empresa_seguridad.id_empresa"))

    empresa = relationship("EmpresaSeguridad", back_populates="centros")
    eventos = relationship("Evento", back_populates="centro")


class Dispositivo(Base):
    __tablename__ = "dispositivo"

    id_dispositivo = Column(Integer, primary_key=True, index=True)
    nombre_dispositivo = Column(String(255), nullable=False)
    tipo_dispositivo = Column(String(100))
    estado = Column(String(50))
    id_ubicacion = Column(Integer, ForeignKey("ubicacion.id_ubicacion"))

    ubicacion = relationship("Ubicacion", back_populates="dispositivos")
    eventos = relationship("Evento", back_populates="dispositivo")


class NivelRiesgo(Base):
    __tablename__ = "nivel_riesgo"

    id_nivel_riesgo = Column(Integer, primary_key=True, index=True)
    nivel = Column(String(100), nullable=False)
    puntaje = Column(Integer)
    descripcion = Column(Text)

    eventos = relationship("Evento", back_populates="nivel_riesgo")


class TipoEvento(Base):
    __tablename__ = "tipo_evento"

    id_tipo_evento = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text)

    eventos = relationship("Evento", back_populates="tipo_evento")


class FuenteEvento(Base):
    __tablename__ = "fuente_evento"

    id_fuente_evento = Column(Integer, primary_key=True, index=True)
    nombre_fuente = Column(String(255), nullable=False)
    tipo_fuente = Column(String(100))
    descripcion = Column(Text)

    eventos = relationship("Evento", back_populates="fuente_evento")


class Evento(Base):
    __tablename__ = "evento"

    id_evento = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    descripcion = Column(Text)
    estado = Column(String(50))
    id_tipo_evento = Column(Integer, ForeignKey("tipo_evento.id_tipo_evento"))
    id_dispositivo = Column(Integer, ForeignKey("dispositivo.id_dispositivo"))
    id_nivel_riesgo = Column(Integer, ForeignKey("nivel_riesgo.id_nivel_riesgo"))
    id_centro = Column(Integer, ForeignKey("centro_monitoreo.id_centro"))
    id_fuente_evento = Column(Integer, ForeignKey("fuente_evento.id_fuente_evento"))
    id_ubicacion = Column(Integer, ForeignKey("ubicacion.id_ubicacion"))

    tipo_evento = relationship("TipoEvento", back_populates="eventos")
    dispositivo = relationship("Dispositivo", back_populates="eventos")
    nivel_riesgo = relationship("NivelRiesgo", back_populates="eventos")
    centro = relationship("CentroMonitoreo", back_populates="eventos")
    fuente_evento = relationship("FuenteEvento", back_populates="eventos")
    ubicacion = relationship("Ubicacion", back_populates="eventos")
    auditorias = relationship("Auditoria", back_populates="evento")
    usuarios_roles = relationship("UsuarioRol", back_populates="evento")


class Auditoria(Base):
    __tablename__ = "auditoria"

    id_auditoria = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    accion = Column(String(100))
    descripcion = Column(Text)
    ip_usuario = Column(String(50))
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    id_evento = Column(Integer, ForeignKey("evento.id_evento"))

    usuario = relationship("Usuario", back_populates="auditorias")
    evento = relationship("Evento", back_populates="auditorias")


class Rol(Base):
    __tablename__ = "rol"

    id_rol = Column(Integer, primary_key=True, index=True)
    nombre_rol = Column(String(150), nullable=False)
    descripcion = Column(Text)

    permisos = relationship("RolPermiso", back_populates="rol")
    usuarios = relationship("UsuarioRol", back_populates="rol")


class Permiso(Base):
    __tablename__ = "permiso"

    id_permiso = Column(Integer, primary_key=True, index=True)  # corregido: id_rol -> id_permiso
    nombre_permiso = Column(String(150), nullable=False)
    descripcion = Column(Text)

    roles = relationship("RolPermiso", back_populates="permiso")


class RolPermiso(Base):
    __tablename__ = "rol_permiso"

    id_rol_permiso = Column(Integer, primary_key=True, index=True)
    id_rol = Column(Integer, ForeignKey("rol.id_rol"))
    id_permiso = Column(Integer, ForeignKey("permiso.id_permiso"))

    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    apellido = Column(String(150))
    correo = Column(String(255), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    estado = Column(String(50))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    roles = relationship("UsuarioRol", back_populates="usuario")
    auditorias = relationship("Auditoria", back_populates="usuario")


class UsuarioRol(Base):
    __tablename__ = "usuario_rol"

    id_usuario_rol = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id_usuario"))
    id_rol = Column(Integer, ForeignKey("rol.id_rol"))
    id_evento = Column(Integer, ForeignKey("evento.id_evento"), nullable=True)

    usuario = relationship("Usuario", back_populates="roles")
    rol = relationship("Rol", back_populates="usuarios")
    evento = relationship("Evento", back_populates="usuarios_roles")
