from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import CentroMonitoreo
from app.dtos import CentroCreate, CentroOut, CentroUpdate
from app.services.crud import actualizar, crear, eliminar, listar_paginado, obtener_o_404
from app.services.validators import validar_referencias


router = APIRouter()


@router.post("/centros/", response_model=CentroOut, status_code=201, tags=["Centro Monitoreo"])
def crear_centro(data: CentroCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    return crear(db, CentroMonitoreo, valores)


@router.get("/centros/", response_model=List[CentroOut], tags=["Centro Monitoreo"])
def listar_centros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar_paginado(db, CentroMonitoreo, skip, limit)


@router.get("/centros/{id}", response_model=CentroOut, tags=["Centro Monitoreo"])
def obtener_centro(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, CentroMonitoreo, CentroMonitoreo.id_centro, id, "Centro no encontrado")


@router.put("/centros/{id}", response_model=CentroOut, tags=["Centro Monitoreo"])
def actualizar_centro(id: int, data: CentroUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, CentroMonitoreo, CentroMonitoreo.id_centro, id, "Centro no encontrado")
    valores = data.model_dump(exclude_unset=True)
    validar_referencias(db, valores)
    return actualizar(db, obj, valores)


@router.delete("/centros/{id}", status_code=204, tags=["Centro Monitoreo"])
def eliminar_centro(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, CentroMonitoreo, CentroMonitoreo.id_centro, id, "Centro no encontrado")
    eliminar(db, obj)
