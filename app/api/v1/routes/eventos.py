from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Auditoria, Evento
from app.schemas.schemas import AuditoriaCreate, AuditoriaOut, EventoCreate, EventoOut, EventoUpdate
from app.services.crud import actualizar, crear, eliminar, listar_paginado, obtener_o_404
from app.services.validators import validar_referencias


router = APIRouter()


@router.post("/eventos/", response_model=EventoOut, status_code=201, tags=["Evento"])
def crear_evento(data: EventoCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    return crear(db, Evento, valores)


@router.get("/eventos/", response_model=List[EventoOut], tags=["Evento"])
def listar_eventos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar_paginado(db, Evento, skip, limit)


@router.get("/eventos/{id}", response_model=EventoOut, tags=["Evento"])
def obtener_evento(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, Evento, Evento.id_evento, id, "Evento no encontrado")


@router.put("/eventos/{id}", response_model=EventoOut, tags=["Evento"])
def actualizar_evento(id: int, data: EventoUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Evento, Evento.id_evento, id, "Evento no encontrado")
    valores = data.model_dump(exclude_unset=True)
    validar_referencias(db, valores)
    return actualizar(db, obj, valores)


@router.delete("/eventos/{id}", status_code=204, tags=["Evento"])
def eliminar_evento(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Evento, Evento.id_evento, id, "Evento no encontrado")
    eliminar(db, obj)


@router.post("/auditorias/", response_model=AuditoriaOut, status_code=201, tags=["Auditoría"])
def crear_auditoria(data: AuditoriaCreate, db: Session = Depends(get_db)):
    valores = data.model_dump()
    validar_referencias(db, valores)
    return crear(db, Auditoria, valores)


@router.get("/auditorias/", response_model=List[AuditoriaOut], tags=["Auditoría"])
def listar_auditorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar_paginado(db, Auditoria, skip, limit)


@router.get("/auditorias/{id}", response_model=AuditoriaOut, tags=["Auditoría"])
def obtener_auditoria(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, Auditoria, Auditoria.id_auditoria, id, "Auditoría no encontrada")


@router.delete("/auditorias/{id}", status_code=204, tags=["Auditoría"])
def eliminar_auditoria(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, Auditoria, Auditoria.id_auditoria, id, "Auditoría no encontrada")
    eliminar(db, obj)
