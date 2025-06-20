from sqlalchemy.orm import Session, joinedload
from Modelo.Producto import Producto
from typing import List, Optional

from Modelo.ProductoAtributo import ProductoAtributo
from Modelo.ProductoImagen import ProductoImagen
from Schema.Producto import ProductoCreate


class ProductoRepo:
    @staticmethod
    def fetch_by_id(db: Session, producto_id: int) -> Optional[Producto]:
        return db.query(Producto).filter(Producto.id == producto_id).first()

    def fetch_by_id_personalizado(db: Session, producto_id: int) -> Optional[dict]:
        producto = (
            db.query(Producto)
            .filter(Producto.id == producto_id)
            .options(
                joinedload(Producto.categoria),
                joinedload(Producto.usuario_creador),
                joinedload(Producto.atributos),
                joinedload(Producto.imagenes),
                joinedload(Producto.reviews)
            )
            .first()
        )

        if not producto:
            return None

        # Agrupamos los atributos
        atributos_agrupados = {}
        for attr in producto.atributos:
            if attr.nombre not in atributos_agrupados:
                atributos_agrupados[attr.nombre] = []
            atributos_agrupados[attr.nombre].append({
                "id": attr.id,
                "valor": attr.valor,
                "precio": attr.precio,
                "cantidad": attr.cantidad
            })

        atributos_formateados = [
            {"nombre": nombre, "valores": valores}
            for nombre, valores in atributos_agrupados.items()
        ]

        # Creamos la respuesta personalizada como dict
        return {
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock,
            "requiere_edad": producto.requiere_edad,
            "descripcion": producto.descripcion,
            "img_portada": producto.img_portada,
            "calificacion": producto.calificacion,
            "creado_en": producto.creado_en,
            "categoria": {
                "id": producto.categoria.id,
                "nombre": producto.categoria.nombre,
            } if producto.categoria else None,
            "usuario_creador": {
                "id": producto.usuario_creador.id,
                "nombre": producto.usuario_creador.nombre,
                "email": producto.usuario_creador.email
            } if producto.usuario_creador else None,
            "imagenes": [
                {
                    "id": img.id,
                    "url": img.url,
                }
                for img in producto.imagenes
            ],
            "reviews": [
                {
                    "id": review.id,
                    "comentario": review.comentario,
                    "calificacion": review.calificacion,
                    "usuario": {
                        "id": review.usuario.id,
                        "nombre": review.usuario.nombre
                    } if review.usuario else None
                }
                for review in producto.reviews
            ],
            "atributos": atributos_formateados
        }

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
            #categoria_id=producto_data.categoria_id,
            requiere_edad=producto_data.requiere_edad,
            imagen_portada=producto_data.img_portada
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
