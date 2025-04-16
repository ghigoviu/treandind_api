from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Repositorio.Orden import OrdenRepo
from Schema.Orden import OrdenCreate, OrdenRead
from ControladorRest import get_db


class OrdenRest:
    router = APIRouter(prefix="/ordenes", tags=["Ordenes"])

    @router.post("/", response_model=OrdenRead)
    def create_orden(orden_data: OrdenCreate, db: Session = Depends(get_db)):
        try:
            return OrdenRepo.create(db, orden_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error al crear la orden: {str(e)}")

    @router.get("/", response_model=List[OrdenRead])
    def get_all_ordenes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return OrdenRepo.fetch_all(db, skip=skip, limit=limit)

    @router.get("/{orden_id}", response_model=OrdenRead)
    def get_orden_by_id(orden_id: int, db: Session = Depends(get_db)):
        orden = OrdenRepo.fetch_by_id(db, orden_id)
        if not orden:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        return orden
