from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.session_utils import confirmar_cambios, eliminar_objeto, guardar_objeto


def obtener_o_404(db: Session, model, columna, valor, detalle: str):
    obj = db.query(model).filter(columna == valor).first()
    if not obj:
        raise HTTPException(status_code=404, detail=detalle)
    return obj


def listar_paginado(db: Session, model, skip: int = 0, limit: int = 100):
    return db.query(model).offset(skip).limit(limit).all()


def listar_todos(db: Session, model):
    return db.query(model).all()


def crear(db: Session, model, valores: dict):
    obj = model(**valores)
    return guardar_objeto(db, obj)


def actualizar(db: Session, obj, valores: dict):
    for campo, valor in valores.items():
        setattr(obj, campo, valor)
    return confirmar_cambios(db, obj)


def eliminar(db: Session, obj) -> None:
    eliminar_objeto(db, obj)
