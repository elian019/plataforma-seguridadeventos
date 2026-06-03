from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Ubicacion
from app.schemas.schemas import UbicacionCreate, UbicacionOut, UbicacionUpdate
from app.services.crud import actualizar, crear, eliminar, listar_paginado, obtener_o_404


router = APIRouter()


@router.post("/ubicaciones/", response_model=UbicacionOut, status_code=status.HTTP_201_CREATED, tags=["Ubicación"])
def crear_ubicacion(data: UbicacionCreate, db: Session = Depends(get_db)):
    return crear(db, Ubicacion, data.model_dump())


@router.get("/ubicaciones/", response_model=List[UbicacionOut], tags=["Ubicación"])
def listar_ubicaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar_paginado(db, Ubicacion, skip, limit)


@router.get("/ubicaciones/{id}", response_model=UbicacionOut, tags=["Ubicación"])
def obtener_ubicacion(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, Ubicacion, Ubicacion.id_ubicacion, id, "Ubicación no encontrada")


@router.put("/ubicaciones/{id}", response_model=UbicacionOut, tags=["Ubicación"])
def actualizar_ubicacion(id: int, data: UbicacionUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Ubicacion, Ubicacion.id_ubicacion, id, "Ubicación no encontrada")
    return actualizar(db, obj, data.model_dump(exclude_unset=True))


@router.delete("/ubicaciones/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Ubicación"])
def eliminar_ubicacion(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Ubicacion, Ubicacion.id_ubicacion, id, "Ubicación no encontrada")
    eliminar(db, obj)
