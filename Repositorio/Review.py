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
        review = Review(**review_data)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    @staticmethod
    def update(db: Session, review_id: int, review_data: dict) -> Optional[Review]:
        review = db.query(Review).filter(Review.id == review_id).first()
        if review:
            for key, value in review_data.items():
                setattr(review, key, value)
            db.commit()
            db.refresh(review)
            return review
        return None

    @staticmethod
    def delete(db: Session, review_id: int, usuario_id: int) -> Optional[Review]:
        review = db.query(Review).filter(Review.id == review_id).first()
        if review:
            if review.usuario_id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes permiso para eliminar este review."
                )
            db.delete(review)
            db.commit()
            ReviewRepo._actualizar_promedio(db, review)
            return review
        return None

    @staticmethod
    def _actualizar_promedio(db: Session, review: Review):
        if review.producto_id:
            reviews = db.query(Review).filter(Review.producto_id == review.producto_id).all()
            promedio = round(mean([r.calificacion for r in reviews]), 2)
            producto = db.query(Producto).filter(Producto.id == review.producto_id).first()
            if producto:
                producto.calificacion = promedio
                db.commit()
        elif review.evento_id:
            reviews = db.query(Review).filter(Review.evento_id == review.evento_id).all()
            promedio = round(mean([r.calificacion for r in reviews]), 2)
            evento = db.query(Evento).filter(Evento.id == review.evento_id).first()
            if evento:
                evento.calificacion = promedio
                db.commit()
