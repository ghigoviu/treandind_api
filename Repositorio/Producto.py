from sqlalchemy.orm import Session
from Modelo import Producto
from typing import List, Optional

class ProductoRepo:
    @staticmethod
    def fetch_by_id(db: Session, producto_id: int) -> Optional[Producto]:
        return db.query(Producto).filter(Producto.id == producto_id).first()

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> List[Producto]:
        return db.query(Producto).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, producto_data: dict) -> Producto:
        producto = Producto(**producto_data)
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def update(db: Session, producto_id: int, producto_data: dict) -> Optional[Producto]:
        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if producto:
            for key, value in producto_data.items():
                setattr(producto, key, value)
            db.commit()
            db.refresh(producto)
            return producto
        return None

    @staticmethod
    def delete(db: Session, producto_id: int) -> Optional[Producto]:
        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if producto:
            db.delete(producto)
            db.commit()
            return producto
        return None
