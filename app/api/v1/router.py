from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.api.v1.routes import catalogos, centros, dispositivos, empresas, eventos, seguridad, ubicaciones


router = APIRouter()
protected_router = APIRouter(dependencies=[Depends(get_current_user)])

router.include_router(seguridad.auth_router)

protected_router.include_router(ubicaciones.router)
protected_router.include_router(empresas.router)
protected_router.include_router(centros.router)
protected_router.include_router(dispositivos.router)
protected_router.include_router(catalogos.router)
protected_router.include_router(eventos.router)
protected_router.include_router(seguridad.router)

router.include_router(protected_router)
