from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import FuenteEvento, NivelRiesgo, TipoEvento
from app.schemas.schemas import (
    FuenteEventoCreate,
    FuenteEventoOut,
    FuenteEventoUpdate,
    NivelRiesgoCreate,
    NivelRiesgoOut,
    NivelRiesgoUpdate,
    TipoEventoCreate,
    TipoEventoOut,
    TipoEventoUpdate,
)
from app.services.crud import actualizar, crear, eliminar, listar_todos, obtener_o_404


router = APIRouter()


@router.post("/niveles-riesgo/", response_model=NivelRiesgoOut, status_code=201, tags=["Nivel Riesgo"])
def crear_nivel_riesgo(data: NivelRiesgoCreate, db: Session = Depends(get_db)):
    return crear(db, NivelRiesgo, data.model_dump())


@router.get("/niveles-riesgo/", response_model=List[NivelRiesgoOut], tags=["Nivel Riesgo"])
def listar_niveles_riesgo(db: Session = Depends(get_db)):
    return listar_todos(db, NivelRiesgo)


@router.get("/niveles-riesgo/{id}", response_model=NivelRiesgoOut, tags=["Nivel Riesgo"])
def obtener_nivel_riesgo(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(
        db,
        NivelRiesgo,
        NivelRiesgo.id_nivel_riesgo,
        id,
        "Nivel de riesgo no encontrado",
    )


@router.put("/niveles-riesgo/{id}", response_model=NivelRiesgoOut, tags=["Nivel Riesgo"])
def actualizar_nivel_riesgo(id: int, data: NivelRiesgoUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(
        db,
        NivelRiesgo,
        NivelRiesgo.id_nivel_riesgo,
        id,
        "Nivel de riesgo no encontrado",
    )
    return actualizar(db, obj, data.model_dump(exclude_unset=True))


@router.delete("/niveles-riesgo/{id}", status_code=204, tags=["Nivel Riesgo"])
def eliminar_nivel_riesgo(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(
        db,
        NivelRiesgo,
        NivelRiesgo.id_nivel_riesgo,
        id,
        "Nivel de riesgo no encontrado",
    )
    eliminar(db, obj)


@router.post("/tipos-evento/", response_model=TipoEventoOut, status_code=201, tags=["Tipo Evento"])
def crear_tipo_evento(data: TipoEventoCreate, db: Session = Depends(get_db)):
    return crear(db, TipoEvento, data.model_dump())


@router.get("/tipos-evento/", response_model=List[TipoEventoOut], tags=["Tipo Evento"])
def listar_tipos_evento(db: Session = Depends(get_db)):
    return listar_todos(db, TipoEvento)


@router.get("/tipos-evento/{id}", response_model=TipoEventoOut, tags=["Tipo Evento"])
def obtener_tipo_evento(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(db, TipoEvento, TipoEvento.id_tipo_evento, id, "Tipo de evento no encontrado")


@router.put("/tipos-evento/{id}", response_model=TipoEventoOut, tags=["Tipo Evento"])
def actualizar_tipo_evento(id: int, data: TipoEventoUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, TipoEvento, TipoEvento.id_tipo_evento, id, "Tipo de evento no encontrado")
    return actualizar(db, obj, data.model_dump(exclude_unset=True))


@router.delete("/tipos-evento/{id}", status_code=204, tags=["Tipo Evento"])
def eliminar_tipo_evento(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(db, TipoEvento, TipoEvento.id_tipo_evento, id, "Tipo de evento no encontrado")
    eliminar(db, obj)


@router.post("/fuentes-evento/", response_model=FuenteEventoOut, status_code=201, tags=["Fuente Evento"])
def crear_fuente_evento(data: FuenteEventoCreate, db: Session = Depends(get_db)):
    return crear(db, FuenteEvento, data.model_dump())


@router.get("/fuentes-evento/", response_model=List[FuenteEventoOut], tags=["Fuente Evento"])
def listar_fuentes_evento(db: Session = Depends(get_db)):
    return listar_todos(db, FuenteEvento)


@router.get("/fuentes-evento/{id}", response_model=FuenteEventoOut, tags=["Fuente Evento"])
def obtener_fuente_evento(id: int, db: Session = Depends(get_db)):
    return obtener_o_404(
        db,
        FuenteEvento,
        FuenteEvento.id_fuente_evento,
        id,
        "Fuente de evento no encontrada",
    )


@router.put("/fuentes-evento/{id}", response_model=FuenteEventoOut, tags=["Fuente Evento"])
def actualizar_fuente_evento(id: int, data: FuenteEventoUpdate, db: Session = Depends(get_db)):
    obj = obtener_o_404(
        db,
        FuenteEvento,
        FuenteEvento.id_fuente_evento,
        id,
        "Fuente de evento no encontrada",
    )
    return actualizar(db, obj, data.model_dump(exclude_unset=True))


@router.delete("/fuentes-evento/{id}", status_code=204, tags=["Fuente Evento"])
def eliminar_fuente_evento(id: int, db: Session = Depends(get_db)):
    obj = obtener_o_404(
        db,
        FuenteEvento,
        FuenteEvento.id_fuente_evento,
        id,
        "Fuente de evento no encontrada",
    )
    eliminar(db, obj)
