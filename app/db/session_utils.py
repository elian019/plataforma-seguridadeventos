from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def confirmar_cambios(db: Session, obj=None):
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto de integridad en los datos") from exc

    if obj is not None:
        db.refresh(obj)
    return obj


def guardar_objeto(db: Session, obj):
    db.add(obj)
    return confirmar_cambios(db, obj)


def eliminar_objeto(db: Session, obj) -> None:
    db.delete(obj)
    confirmar_cambios(db)
