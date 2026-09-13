from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from Schema.Membresia import (
    PaqueteCreate, PaqueteRead, SuscribirRequest, SuscripcionRead,
)
from Repositorio.Membresia import MembresiaRepo
from Repositorio.Producto import ProductoRepo
from Schema.Producto import ProductoRead
from ControladorRest import get_db


class MembresiaRest:
    router = APIRouter(prefix="/membresias", tags=["Membresias"])

    @router.post("/paquetes", response_model=PaqueteRead, status_code=201)
    def crear_paquete(body: PaqueteCreate, db: Session = Depends(get_db)):
        return MembresiaRepo.crear_paquete(db, body.dict())

    @router.get("/paquetes/vendedor/{vendedor_id}", response_model=List[PaqueteRead])
    def paquetes_por_vendedor(vendedor_id: int, db: Session = Depends(get_db)):
        return MembresiaRepo.fetch_paquetes_por_vendedor(db, vendedor_id)

    @router.post("/suscribir", response_model=SuscripcionRead, status_code=201)
    def suscribir(body: SuscribirRequest, db: Session = Depends(get_db)):
        return MembresiaRepo.suscribir(db, body.usuario_id, body.paquete_id)

    @router.get("/usuario/{usuario_id}/suscripciones", response_model=List[SuscripcionRead])
    def suscripciones_usuario(usuario_id: int, db: Session = Depends(get_db)):
        return MembresiaRepo.fetch_suscripciones_usuario(db, usuario_id)

    @router.get("/vip/vendedor/{vendedor_id}/solicitante/{solicitante_id}", response_model=List[ProductoRead])
    def productos_vip(vendedor_id: int, solicitante_id: int, db: Session = Depends(get_db)):
        """Productos VIP del vendedor, visibles solo si el solicitante está suscrito."""
        return ProductoRepo.fetch_vip_por_vendedor(db, vendedor_id, solicitante_id)

    @router.post("/procesar-vencimientos")
    def procesar_vencimientos(dias_alerta: int = 7, db: Session = Depends(get_db)):
        """Marca suscripciones vencidas y alerta las próximas a vencer."""
        return MembresiaRepo.procesar_vencimientos(db, dias_alerta)
