from sqlalchemy.orm import Session, joinedload
from Modelo.Evento import Evento
from typing import List, Optional

from Modelo.EventoAsistente import EventoAsistente


class EventoRepo:
    @staticmethod
    def fetch_by_id(db: Session, evento_id: int) -> Optional[Evento]:
        return db.query(Evento).filter(Evento.id == evento_id).first()

    @staticmethod
    def registrar_asistente(db: Session, evento_id: int, usuario_id: int) -> EventoAsistente:
        asistente = EventoAsistente(
            evento_id=evento_id,
            usuario_id=usuario_id,
            estado='pendiente'
        )
        db.add(asistente)
        db.commit()
        db.refresh(asistente)
        return asistente

    @staticmethod
    def fetch_con_asistentes(db: Session, evento_id: int) -> Optional[Evento]:
        return db.query(Evento) \
            .options(joinedload(Evento.asistentes)) \
            .filter(Evento.id == evento_id) \
            .first()

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
