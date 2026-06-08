from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Dispositivo
from app.dtos import DispositivoCreate, DispositivoOut, DispositivoUpdate
from app.services.crud import actualizar, crear, eliminar, listar_paginado, obtener_o_404
from app.services.validators import validar_referencias


router = APIRouter()


@router.post("/dispositivos/", response_model=DispositivoOut, status_code=201, tags=["Dispositivo"])
def crear_dispositivo(data: DispositivoCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    return crear(db, Dispositivo, valores)


@router.get("/dispositivos/", response_model=List[DispositivoOut], tags=["Dispositivo"])
def listar_dispositivos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar_paginado(db, Dispositivo, skip, limit)


@router.get("/dispositivos/{id}", response_model=DispositivoOut, tags=["Dispositivo"])
def obtener_dispositivo(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, Dispositivo, Dispositivo.id_dispositivo, id, "Dispositivo no encontrado")


@router.put("/dispositivos/{id}", response_model=DispositivoOut, tags=["Dispositivo"])
def actualizar_dispositivo(id: int, data: DispositivoUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Dispositivo, Dispositivo.id_dispositivo, id, "Dispositivo no encontrado")
    valores = data.model_dump(exclude_unset=True)
    validar_referencias(db, valores)
    return actualizar(db, obj, valores)


@router.delete("/dispositivos/{id}", status_code=204, tags=["Dispositivo"])
def eliminar_dispositivo(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Dispositivo, Dispositivo.id_dispositivo, id, "Dispositivo no encontrado")
    eliminar(db, obj)
