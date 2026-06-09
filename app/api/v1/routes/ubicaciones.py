from typing import List

from fastapi import APIRouter, Depends, Query, status
from geoalchemy2 import Geography
from sqlalchemy import cast, func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import Ubicacion
from app.dtos import (
    UbicacionConDistanciaOut,
    UbicacionCreate,
    UbicacionOut,
    UbicacionUpdate,
)
from app.services.crud import actualizar, crear, eliminar, listar_paginado, obtener_o_404


router = APIRouter()


@router.post("/ubicaciones/", response_model=UbicacionOut, status_code=status.HTTP_201_CREATED, tags=["Ubicación"])
def crear_ubicacion(data: UbicacionCreate, db: Session = Depends(get_db)):
    return crear(db, Ubicacion, data.model_dump())


@router.get("/ubicaciones/", response_model=List[UbicacionOut], tags=["Ubicación"])
def listar_ubicaciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return listar_paginado(db, Ubicacion, skip, limit)


@router.get("/ubicaciones/cercanas/", response_model=List[UbicacionConDistanciaOut], tags=["Ubicación"])
def listar_ubicaciones_cercanas(
    latitud: float = Query(..., ge=-90, le=90),
    longitud: float = Query(..., ge=-180, le=180),
    radio_metros: float = Query(..., gt=0, le=1000000),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    punto = func.ST_SetSRID(func.ST_MakePoint(longitud, latitud), 4326)
    punto_geog = cast(punto, Geography(geometry_type="POINT", srid=4326))
    distancia_metros = func.ST_Distance(Ubicacion.geog, punto_geog).label("distancia_metros")

    resultados = (
        db.query(Ubicacion, distancia_metros)
        .filter(Ubicacion.geog.isnot(None))
        .filter(func.ST_DWithin(Ubicacion.geog, punto_geog, radio_metros))
        .order_by(distancia_metros)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        {
            "id_ubicacion": ubicacion.id_ubicacion,
            "direccion": ubicacion.direccion,
            "zona": ubicacion.zona,
            "latitud": ubicacion.latitud,
            "longitud": ubicacion.longitud,
            "referencia": ubicacion.referencia,
            "distancia_metros": distancia,
        }
        for ubicacion, distancia in resultados
    ]


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
