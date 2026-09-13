from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Repositorio.Orden import OrdenRepo
from Schema.Orden import OrdenCreate, OrdenRead, OrdenDetalleRead, CompraRequest
from ControladorRest import get_db


class OrdenRest:
    router = APIRouter(prefix="/ordenes", tags=["Ordenes"])

    @router.post("/", response_model=OrdenRead)
    def create_orden(orden_data: OrdenCreate, db: Session = Depends(get_db)):
        try:
            return OrdenRepo.create(db, orden_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al crear la orden: {str(e)}")

    @router.post("/comprar", response_model=OrdenRead, status_code=201)
    def comprar(body: CompraRequest, db: Session = Depends(get_db)):
        """Compra directa de un producto: crea la orden y descuenta stock."""
        return OrdenRepo.comprar(db, body.usuario_id, body.producto_id, body.cantidad)

    @router.get("/", response_model=List[OrdenRead])
    def get_all_ordenes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return OrdenRepo.fetch_all(db)

    @router.get("/usuario/{usuario_id}", response_model=List[OrdenRead])
    def get_ordenes_by_usuario(usuario_id: int, db: Session = Depends(get_db)):
        """Historial de compras de un usuario."""
        return OrdenRepo.fetch_by_usuario(db, usuario_id)

    @router.get("/vendedor/{vendedor_id}/ventas")
    def get_ventas_by_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
        """Ventas de los productos publicados por un vendedor."""
        return OrdenRepo.fetch_ventas_por_vendedor(db, vendedor_id)

    @router.get("/{orden_id}/detalles", response_model=List[OrdenDetalleRead])
    def get_detalles_orden(orden_id: int, db: Session = Depends(get_db)):
        return OrdenRepo.fetch_detalles(db, orden_id)

    @router.get("/{orden_id}", response_model=OrdenRead)
    def get_orden_by_id(orden_id: int, db: Session = Depends(get_db)):
        orden = OrdenRepo.fetch_by_id(db, orden_id)
        if not orden:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        return orden
