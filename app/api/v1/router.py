from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.api.v1.routes import catalogos, centros, dispositivos, empresas, eventos, seguridad, ubicaciones


router = APIRouter(dependencies=[Depends(get_current_user)])

router.include_router(ubicaciones.router)
router.include_router(empresas.router)
router.include_router(centros.router)
router.include_router(dispositivos.router)
router.include_router(catalogos.router)
router.include_router(eventos.router)
router.include_router(seguridad.router)
