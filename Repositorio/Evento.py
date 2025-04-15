from sqlalchemy.orm import Session
from Modelo import Evento
from typing import List, Optional


class EventoRepo:
    @staticmethod
    def fetch_by_id(db: Session, evento_id: int) -> Optional[Evento]:
        return db.query(Evento).filter(Evento.id == evento_id).first()

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> List[Evento]:
        return db.query(Evento).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, evento_data: dict) -> Evento:
        evento = Evento(**evento_data)
        db.add(evento)
        db.commit()
        db.refresh(evento)
        return evento

    @staticmethod
    def update(db: Session, evento_id: int, evento_data: dict) -> Optional[Evento]:
        evento = db.query(Evento).filter(Evento.id == evento_id).first()
        if evento:
            for key, value in evento_data.items():
                setattr(evento, key, value)
            db.commit()
            db.refresh(evento)
            return evento
        return None

    @staticmethod
    def delete(db: Session, evento_id: int) -> Optional[Evento]:
        evento = db.query(Evento).filter(Evento.id == evento_id).first()
        if evento:
            db.delete(evento)
            db.commit()
            return evento
        return None
