from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Modelo.Orden import Orden
from Modelo.OrdenDetalle import OrdenDetalle
from Schema.Orden import OrdenCreate
from typing import Optional, List
from fastapi import HTTPException


class OrdenRepo:
    @staticmethod
    def fetch_by_id(db: Session, orden_id: int) -> Optional[Orden]:
        return db.query(Orden).filter(Orden.id == orden_id).first()

    @staticmethod
    def fetch_all(db: Session) -> List[Orden]:
        return db.query(Orden).all()

    @staticmethod
    def create(db: Session, orden_data: OrdenCreate) -> Orden:
        try:
            orden_dict = orden_data.orden.dict()
            detalles = orden_data.detalles

            orden = Orden(**orden_dict)
            db.add(orden)
            db.flush()  # Para obtener orden.id antes de insertar detalles

            for detalle_data in detalles:
                detalle_dict = detalle_data.dict()
                detalle = OrdenDetalle(orden_id=orden.id, **detalle_dict)
                db.add(detalle)

            db.commit()
            db.refresh(orden)
            return orden

        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error al crear la orden: " + str(e))

    @staticmethod
    def delete(db: Session, orden_id: int) -> Optional[Orden]:
        orden = db.query(Orden).filter(Orden.id == orden_id).first()
        if orden:
            db.delete(orden)
            db.commit()
            return orden
        return None
