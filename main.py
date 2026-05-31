from fastapi import FastAPI

app = FastAPI(
    title="Plataforma Seguridad Eventos",
    description="API para la gestión y monitoreo de eventos de seguridad.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Bienvenido a la Plataforma Seguridad Eventos",
        "status": "online"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
