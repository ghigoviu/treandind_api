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
        from fastapi import HTTPException, status

        evento = db.query(Evento).filter(Evento.id == evento_id).first()
        if not evento:
            raise HTTPException(status_code=404, detail="Evento no encontrado.")

        # Validar disponibilidad de boletos (si el evento maneja boletos).
        if evento.boletos_total > 0 and evento.boletos_disponibles <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay boletos disponibles para este evento."
            )

        asistente = EventoAsistente(
            evento_id=evento_id,
            usuario_id=usuario_id,
            estado='pendiente'
        )
        db.add(asistente)
        # Descontar un boleto de forma atómica (mismo commit).
        if evento.boletos_total > 0:
            evento.boletos_disponibles -= 1
        db.commit()
        db.refresh(asistente)
        return asistente

    @staticmethod
    def fetch_by_vendedor(db: Session, usuario_id: int) -> List[Evento]:
        return db.query(Evento).filter(Evento.usuario_id == usuario_id).all()

    @staticmethod
    def fetch_suscritos(db: Session, usuario_id: int) -> List[Evento]:
        """Eventos a los que el usuario se ha suscrito (es asistente)."""
        return (
            db.query(Evento)
            .join(EventoAsistente, EventoAsistente.evento_id == Evento.id)
            .filter(EventoAsistente.usuario_id == usuario_id)
            .order_by(Evento.fecha.asc())
            .all()
        )

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
