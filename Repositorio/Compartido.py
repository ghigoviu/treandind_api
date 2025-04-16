from sqlalchemy.orm import Session
from typing import List, Optional
from Modelo import Compartido, Amistad
from fastapi import HTTPException, status


class CompartidoRepo:
    @staticmethod
    def fetch_by_id(db: Session, compartido_id: int) -> Optional[Compartido]:
        return db.query(Compartido).filter(Compartido.id == compartido_id).first()

    @staticmethod
    def fetch_all(db: Session) -> List[Compartido]:
        return db.query(Compartido).all()

    @staticmethod
    def create(db: Session, compartido_data: dict) -> Compartido:
        usuario_id = compartido_data.get("usuario_id")
        amigo_id = compartido_data.get("amigo_id")

        #  Validación 1: No se puede compartir a uno mismo
        if usuario_id == amigo_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes compartir contenido contigo mismo."
            )

        #  Validación 2: El amigo debe estar en la lista de amistades del usuario
        amistad = db.query(Amistad).filter(
            Amistad.usuario_id == usuario_id,
            Amistad.amigo_id == amigo_id
        ).first()

        if not amistad:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puedes compartir contenido con alguien que no es tu amigo."
            )

        compartido = Compartido(**compartido_data)
        db.add(compartido)
        db.commit()
        db.refresh(compartido)
        return compartido

    @staticmethod
    def update(db: Session, compartido_id: int, compartido_data: dict) -> Optional[Compartido]:
        compartido = db.query(Compartido).filter(Compartido.id == compartido_id).first()
        if compartido:
            for key, value in compartido_data.items():
                setattr(compartido, key, value)
            db.commit()
            db.refresh(compartido)
            return compartido
        return None
