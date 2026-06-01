from fastapi import FastAPI
from app.db.database import engine
from app.models.models import Base
from app.api.v1.controllers import router

# Crea todas las tablas en la BD si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Seguridad - API",
    description="API REST para gestión de eventos, dispositivos, usuarios y seguridad.",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def root():
    return {"mensaje": "API de Sistema de Seguridad activa", "docs": "/docs"}
