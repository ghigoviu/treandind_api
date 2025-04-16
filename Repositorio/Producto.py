from sqlalchemy.orm import Session
from Modelo.Producto import Producto
from typing import List, Optional

from Modelo.ProductoAtributo import ProductoAtributo
from Modelo.ProductoImagen import ProductoImagen
from Schema.Producto import ProductoCreate


class ProductoRepo:
    @staticmethod
    def fetch_by_id(db: Session, producto_id: int) -> Optional[Producto]:
        return db.query(Producto).filter(Producto.id == producto_id).first()

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> List[Producto]:
        return db.query(Producto).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, producto_data: ProductoCreate) -> Producto:
        producto = Producto(
            nombre=producto_data.nombre,
            descripcion=producto_data.descripcion,
            precio=producto_data.precio,
            stock=producto_data.stock,
            usuario_id=producto_data.usuario_id,
            categoria_id=producto_data.categoria_id,
            requiere_edad=producto_data.requiere_edad,
        )
        db.add(producto)
        db.flush()  # Para obtener el ID antes del commit

        # Crear atributos relacionados
        for attr in producto_data.atributos:
            atributo = ProductoAtributo(
                producto_id=producto.id,
                nombre=attr.nombre,
                valor=attr.valor
            )
            db.add(atributo)

        # Crear imágenes relacionadas
        for img in producto_data.imagenes:
            imagen = ProductoImagen(
                producto_id=producto.id,
                url=img.url,
                es_portada=img.es_portada
            )
            db.add(imagen)

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
