from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Repositorio.Estadistica import EstadisticaRepo
from ControladorRest import get_db


class EstadisticaRest:
    router = APIRouter(prefix="/estadisticas", tags=["Estadisticas"])

    @router.get("/vendedor/{vendedor_id}")
    def resumen_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
        """Dashboard de ventas del vendedor: totales, top productos, top
        compradores y ventas por mes."""
        return EstadisticaRepo.resumen(db, vendedor_id)
