from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import EmpresaSeguridad
from app.dtos import EmpresaCreate, EmpresaOut, EmpresaUpdate
from app.services.crud import actualizar, crear, eliminar, listar_paginado, obtener_o_404


router = APIRouter()


@router.post("/empresas/", response_model=EmpresaOut, status_code=201, tags=["Empresa Seguridad"])
def crear_empresa(data: EmpresaCreate, db: Session = Depends(get_db)):
    return crear(db, EmpresaSeguridad, data.model_dump())


@router.get("/empresas/", response_model=List[EmpresaOut], tags=["Empresa Seguridad"])
def listar_empresas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar_paginado(db, EmpresaSeguridad, skip, limit)


@router.get("/empresas/{id}", response_model=EmpresaOut, tags=["Empresa Seguridad"])
def obtener_empresa(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, EmpresaSeguridad, EmpresaSeguridad.id_empresa, id, "Empresa no encontrada")


@router.put("/empresas/{id}", response_model=EmpresaOut, tags=["Empresa Seguridad"])
def actualizar_empresa(id: int, data: EmpresaUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, EmpresaSeguridad, EmpresaSeguridad.id_empresa, id, "Empresa no encontrada")
    return actualizar(db, obj, data.model_dump(exclude_unset=True))


@router.delete("/empresas/{id}", status_code=204, tags=["Empresa Seguridad"])
def eliminar_empresa(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, EmpresaSeguridad, EmpresaSeguridad.id_empresa, id, "Empresa no encontrada")
    eliminar(db, obj)
