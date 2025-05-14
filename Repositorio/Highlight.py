from sqlalchemy.orm import Session
from typing import Optional, Type
from Modelo.Highlight import Highlight


class HighlightRepo:

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Highlight]]:
        return db.query(Highlight).offset(skip).limit(limit).all()

    @staticmethod
    def fetch_by_id(db: Session, highlight_id: int) -> Optional[Highlight]:
        return db.query(Highlight).filter(Highlight.id == highlight_id).first()

    @staticmethod
    def create(db: Session, highlight_data: dict) -> Highlight:
        nuevo = Highlight(**highlight_data)
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    @staticmethod
    def update(db: Session, highlight_id: int, highlight_data: dict) -> Type[Highlight] | None:
        highlight = db.query(Highlight).filter(Highlight.id == highlight_id).first()
        if highlight:
            for key, value in highlight_data.items():
                setattr(highlight, key, value)
            db.commit()
            db.refresh(highlight)
            return highlight
        return None

    @staticmethod
    def delete(db: Session, highlight_id: int) -> Type[Highlight] | None:
        highlight = db.query(Highlight).filter(Highlight.id == highlight_id).first()
        if highlight:
            db.delete(highlight)
            db.commit()
            return highlight
        return None
