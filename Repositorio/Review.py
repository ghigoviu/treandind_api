from statistics import mean

from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from Modelo.Evento import Evento
from Modelo.Producto import Producto
from Modelo.Review import Review
from typing import List, Optional


class ReviewRepo:
    @staticmethod
    def fetch_by_id(db: Session, review_id: int) -> Optional[Review]:
        return db.query(Review).filter(Review.id == review_id).first()

    @staticmethod
    def fetch_by_producto_id(db: Session, producto_id: int) -> List[Review]:
        return db.query(Review).filter(Review.producto_id == producto_id).all()

    @staticmethod
    def fetch_by_evento_id(db: Session, evento_id: int) -> List[Review]:
        return db.query(Review).filter(Review.evento_id == evento_id).all()

    @staticmethod
    def fetch_by_usuario_id(db: Session, usuario_id: int) -> List[Review]:
        return db.query(Review).filter(Review.usuario_id == usuario_id).all()

    @staticmethod
    def create(db: Session, review_data: dict) -> Review:
        producto_id = review_data.get("producto_id")
        evento_id = review_data.get("evento_id")
        usuario_id = review_data.get("usuario_id")

        # Exactamente uno de producto_id / evento_id debe estar presente.
        if bool(producto_id) == bool(evento_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debes indicar exactamente un producto_id o un evento_id.",
            )

        # Anti-duplicado: un usuario no puede reseñar dos veces el mismo item.
        query = db.query(Review).filter(Review.usuario_id == usuario_id)
        if producto_id:
            query = query.filter(Review.producto_id == producto_id)
        else:
            query = query.filter(Review.evento_id == evento_id)
        if query.first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya has dejado una reseña para este elemento.",
            )

        # Reseña ligada a compra: para productos, el usuario debe haber comprado
        # el producto (existe una orden completada con ese producto).
        if producto_id and not ReviewRepo._usuario_compro_producto(db, usuario_id, producto_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes reseñar productos que hayas comprado.",
            )

        review = Review(
            usuario_id=usuario_id,
            calificacion=review_data.get("calificacion"),
            comentario=review_data.get("comentario"),
            producto_id=producto_id,
            evento_id=evento_id,
        )
        db.add(review)
        db.flush()  # asigna id sin cerrar la transacción
        # Recalcular el promedio dentro de la misma transacción.
        ReviewRepo._actualizar_promedio(db, review)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def update(db: Session, review_id: int, review_data: dict) -> Optional[Review]:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return None
        for key, value in review_data.items():
            # usuario_id no se reasigna en una actualización de contenido.
            if key == "usuario_id":
                continue
            if value is not None:
                setattr(review, key, value)
        db.flush()
        ReviewRepo._actualizar_promedio(db, review)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def delete(db: Session, review_id: int, usuario_id: int) -> Optional[Review]:
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            return None
        if review.usuario_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar este review.",
            )

        # Capturar datos antes de borrar (el objeto queda inaccesible tras commit).
        snapshot = {
            "id": review.id,
            "usuario_id": review.usuario_id,
            "producto_id": review.producto_id,
            "evento_id": review.evento_id,
            "calificacion": review.calificacion,
            "comentario": review.comentario,
        }
        producto_id = review.producto_id
        evento_id = review.evento_id

        db.delete(review)
        db.flush()  # aplica el borrado sin cerrar la transacción
        # Recalcular el promedio del item afectado (atómico con el borrado).
        ReviewRepo._recalcular_item(db, producto_id, evento_id)
        db.commit()
        return snapshot

    @staticmethod
    def _usuario_compro_producto(db: Session, usuario_id: int, producto_id: int) -> bool:
        """True si el usuario tiene alguna orden completada que incluye el producto."""
        from Modelo.Orden import Orden
        from Modelo.OrdenDetalle import OrdenDetalle

        existe = (
            db.query(OrdenDetalle)
            .join(Orden, OrdenDetalle.orden_id == Orden.id)
            .filter(
                Orden.usuario_id == usuario_id,
                Orden.estado == 'completada',
                OrdenDetalle.producto_id == producto_id,
            )
            .first()
        )
        return existe is not None

    # --- Helpers de recálculo de promedio ------------------------------------

    @staticmethod
    def _actualizar_promedio(db: Session, review: Review):
        """Recalcula el promedio del item asociado a la review dada."""
        ReviewRepo._recalcular_item(db, review.producto_id, review.evento_id)

    @staticmethod
    def _recalcular_item(db: Session, producto_id, evento_id):
        """Recalcula la calificación promedio de un producto o evento.

        Maneja el caso de lista vacía (sin reviews) dejando la calificación en 0
        para evitar división por cero. No hace commit: opera dentro de la
        transacción del llamador para garantizar atomicidad.
        """
        if producto_id:
            reviews = db.query(Review).filter(Review.producto_id == producto_id).all()
            promedio = round(mean([r.calificacion for r in reviews]), 2) if reviews else 0.0
            producto = db.query(Producto).filter(Producto.id == producto_id).first()
            if producto:
                producto.calificacion = promedio
        elif evento_id:
            reviews = db.query(Review).filter(Review.evento_id == evento_id).all()
            promedio = round(mean([r.calificacion for r in reviews]), 2) if reviews else 0.0
            evento = db.query(Evento).filter(Evento.id == evento_id).first()
            if evento:
                evento.calificacion = promedio
