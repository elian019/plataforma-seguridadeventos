from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.database import get_db
from app.models.models import Permiso, Rol, RolPermiso, Usuario, UsuarioRol
from app.dtos import (
    LoginRequest,
    PermisoCreate,
    PermisoOut,
    PermisoUpdate,
    RolCreate,
    RolOut,
    RolPermisoCreate,
    RolPermisoOut,
    RolUpdate,
    UsuarioCreate,
    UsuarioOut,
    UsuarioRolCreate,
    UsuarioRolOut,
    UsuarioUpdate,
    TokenOut,
)
from app.services.crud import actualizar, crear, eliminar, listar_paginado, listar_todos, obtener_o_404
from app.services.validators import (
    hash_password_or_422,
    validar_correo_unico,
    validar_referencias,
    validar_relacion_rol_permiso_unica,
    validar_relacion_usuario_rol_unica,
)


auth_router = APIRouter(prefix="/auth", tags=["Auth"])
router = APIRouter()


@auth_router.post("/login", response_model=TokenOut)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == data.correo).first()
    if usuario is None or not verify_password(data.contrasena, usuario.contrasena):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if usuario.estado and usuario.estado.lower() in {"inactivo", "bloqueado", "suspendido"}:
        raise HTTPException(status_code=403, detail="Usuario inactivo o bloqueado")

    access_token = create_access_token(
        subject=str(usuario.id_usuario),
        extra_claims={"correo": usuario.correo},
    )
    return TokenOut(
        access_token=access_token,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/roles/", response_model=RolOut, status_code=201, tags=["Rol"])
def crear_rol(data: RolCreate, db: Session = Depends(get_db)):
    return crear(db, Rol, data.model_dump())


@router.get("/roles/", response_model=List[RolOut], tags=["Rol"])
def listar_roles(db: Session = Depends(get_db)):
    return listar_todos(db, Rol)


@router.get("/roles/{id}", response_model=RolOut, tags=["Rol"])
def obtener_rol(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, Rol, Rol.id_rol, id, "Rol no encontrado")


@router.put("/roles/{id}", response_model=RolOut, tags=["Rol"])
def actualizar_rol(id: int, data: RolUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Rol, Rol.id_rol, id, "Rol no encontrado")
    return actualizar(db, obj, data.model_dump(exclude_unset=True))


@router.delete("/roles/{id}", status_code=204, tags=["Rol"])
def eliminar_rol(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Rol, Rol.id_rol, id, "Rol no encontrado")
    eliminar(db, obj)


@router.post("/permisos/", response_model=PermisoOut, status_code=201, tags=["Permiso"])
def crear_permiso(data: PermisoCreate, db: Session = Depends(get_db)):
    return crear(db, Permiso, data.model_dump())


@router.get("/permisos/", response_model=List[PermisoOut], tags=["Permiso"])
def listar_permisos(db: Session = Depends(get_db)):
    return listar_todos(db, Permiso)


@router.get("/permisos/{id}", response_model=PermisoOut, tags=["Permiso"])
def obtener_permiso(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, Permiso, Permiso.id_permiso, id, "Permiso no encontrado")


@router.put("/permisos/{id}", response_model=PermisoOut, tags=["Permiso"])
def actualizar_permiso(id: int, data: PermisoUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Permiso, Permiso.id_permiso, id, "Permiso no encontrado")
    return actualizar(db, obj, data.model_dump(exclude_unset=True))


@router.delete("/permisos/{id}", status_code=204, tags=["Permiso"])
def eliminar_permiso(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Permiso, Permiso.id_permiso, id, "Permiso no encontrado")
    eliminar(db, obj)


@router.post("/roles-permisos/", response_model=RolPermisoOut, status_code=201, tags=["Rol-Permiso"])
def asignar_permiso_a_rol(data: RolPermisoCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    validar_relacion_rol_permiso_unica(db, valores["id_rol"], valores["id_permiso"])
    return crear(db, RolPermiso, valores)


@router.get("/roles-permisos/", response_model=List[RolPermisoOut], tags=["Rol-Permiso"])
def listar_roles_permisos(db: Session = Depends(get_db)):
    return listar_todos(db, RolPermiso)


@router.delete("/roles-permisos/{id}", status_code=204, tags=["Rol-Permiso"])
def eliminar_rol_permiso(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(
        db,
        RolPermiso,
        RolPermiso.id_rol_permiso,
        id,
        "Relación Rol-Permiso no encontrada",
    )
    eliminar(db, obj)


@router.post("/usuarios/", response_model=UsuarioOut, status_code=201, tags=["Usuario"])
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    validar_correo_unico(db, data.correo)
    valores = data.model_dump()
    valores["contrasena"] = hash_password_or_422(valores["contrasena"])
    return crear(db, Usuario, valores)


@router.get("/usuarios/", response_model=List[UsuarioOut], tags=["Usuario"])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar_paginado(db, Usuario, skip, limit)


@router.get("/usuarios/{id}", response_model=UsuarioOut, tags=["Usuario"])
def obtener_usuario(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, Usuario, Usuario.id_usuario, id, "Usuario no encontrado")


@router.put("/usuarios/{id}", response_model=UsuarioOut, tags=["Usuario"])
def actualizar_usuario(id: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Usuario, Usuario.id_usuario, id, "Usuario no encontrado")
    valores = data.model_dump(exclude_unset=True)

    if "correo" in valores:
        validar_correo_unico(db, valores["correo"], usuario_id=id)
    if "contrasena" in valores:
        valores["contrasena"] = hash_password_or_422(valores["contrasena"])

    return actualizar(db, obj, valores)


@router.delete("/usuarios/{id}", status_code=204, tags=["Usuario"])
def eliminar_usuario(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Usuario, Usuario.id_usuario, id, "Usuario no encontrado")
    eliminar(db, obj)


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
    return crear(db, UsuarioRol, valores)


@router.get("/usuarios-roles/", response_model=List[UsuarioRolOut], tags=["Usuario-Rol"])
def listar_usuarios_roles(db: Session = Depends(get_db)):
    return listar_todos(db, UsuarioRol)


@router.delete("/usuarios-roles/{id}", status_code=204, tags=["Usuario-Rol"])
def eliminar_usuario_rol(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(
        db,
        UsuarioRol,
        UsuarioRol.id_usuario_rol,
        id,
        "Relación Usuario-Rol no encontrada",
    )
    eliminar(db, obj)
