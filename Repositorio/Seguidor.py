from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional

from Modelo.Seguidor import Seguidor
from Modelo.Usuario import Usuario


class SeguidorRepo:

    @staticmethod
    def seguir(db: Session, seguidor_id: int, seguido_id: int) -> Seguidor:
        """Crea un seguimiento. No requiere amistad."""
        if seguidor_id == seguido_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No puedes seguirte a ti mismo."
            )

        existe = db.query(Seguidor).filter(
            Seguidor.seguidor_id == seguidor_id,
            Seguidor.seguido_id == seguido_id,
        ).first()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya sigues a este usuario."
            )

        try:
            s = Seguidor(seguidor_id=seguidor_id, seguido_id=seguido_id)
            db.add(s)
            db.flush()

            # Notificar al usuario seguido.
            from Repositorio.Notificacion import NotificacionRepo
            seguidor = db.query(Usuario).filter(Usuario.id == seguidor_id).first()
            nombre = seguidor.nombre if seguidor else "Alguien"
            NotificacionRepo.crear(
                db, seguido_id, "seguidor",
                f"{nombre} comenzó a seguirte.", ref_id=seguidor_id
            )

            db.commit()
            db.refresh(s)
            return s
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear el seguimiento (usuario inexistente)."
            )

    @staticmethod
    def dejar_de_seguir(db: Session, seguidor_id: int, seguido_id: int) -> bool:
        s = db.query(Seguidor).filter(
            Seguidor.seguidor_id == seguidor_id,
            Seguidor.seguido_id == seguido_id,
        ).first()
        if not s:
            return False
        db.delete(s)
        db.commit()
        return True

    @staticmethod
    def esta_siguiendo(db: Session, seguidor_id: int, seguido_id: int) -> bool:
        return db.query(Seguidor).filter(
            Seguidor.seguidor_id == seguidor_id,
            Seguidor.seguido_id == seguido_id,
        ).first() is not None

    @staticmethod
    def fetch_siguiendo(db: Session, usuario_id: int) -> List[Usuario]:
        """Usuarios a los que sigue (con datos para el frontend)."""
        ids = [
            r[0] for r in
            db.query(Seguidor.seguido_id).filter(Seguidor.seguidor_id == usuario_id).all()
        ]
        if not ids:
            return []
        return db.query(Usuario).filter(Usuario.id.in_(ids)).all()

    @staticmethod
    def fetch_seguidores(db: Session, usuario_id: int) -> List[Usuario]:
        """Usuarios que siguen a este usuario."""
        ids = [
            r[0] for r in
            db.query(Seguidor.seguidor_id).filter(Seguidor.seguido_id == usuario_id).all()
        ]
        if not ids:
            return []
        return db.query(Usuario).filter(Usuario.id.in_(ids)).all()

    @staticmethod
    def contar_siguiendo(db: Session, usuario_id: int) -> int:
        return db.query(Seguidor).filter(Seguidor.seguidor_id == usuario_id).count()

    @staticmethod
    def contar_seguidores(db: Session, usuario_id: int) -> int:
        return db.query(Seguidor).filter(Seguidor.seguido_id == usuario_id).count()

    @staticmethod
    def seguir_silencioso(db: Session, seguidor_id: int, seguido_id: int):
        """Crea seguimiento sin lanzar excepciones si ya existe o son el mismo.
        Usado internamente al aceptar amistad para auto-seguir."""
        if seguidor_id == seguido_id:
            return
        existe = db.query(Seguidor).filter(
            Seguidor.seguidor_id == seguidor_id,
            Seguidor.seguido_id == seguido_id,
        ).first()
        if existe:
            return
        s = Seguidor(seguidor_id=seguidor_id, seguido_id=seguido_id)
        db.add(s)
