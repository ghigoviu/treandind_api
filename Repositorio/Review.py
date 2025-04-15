from sqlalchemy.orm import Session
from Modelo import Review
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
    def delete(db: Session, review_id: int) -> Optional[Review]:
        review = db.query(Review).filter(Review.id == review_id).first()
        if review:
            db.delete(review)
            db.commit()
            return review
        return None
