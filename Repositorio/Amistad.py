from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from typing import List, Type, Optional

from Modelo.Amistad import Amistad


class AmistadRepo:

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> List[Amistad]:
        return db.query(Amistad).offset(skip).limit(limit).all()

    @staticmethod
    def fetch_amigos(db: Session, usuario_id: int) -> List[Amistad]:
        """Amistades aceptadas del usuario, sin importar quién envió la solicitud."""
        return db.query(Amistad).filter(
            Amistad.estado == 'aceptada',
            or_(
                Amistad.usuario_id == usuario_id,
                Amistad.amigo_id == usuario_id,
            )
        ).all()

    @staticmethod
    def fetch_pendientes(db: Session, usuario_id: int) -> List[Amistad]:
        """Solicitudes de amistad pendientes RECIBIDAS por el usuario."""
        return db.query(Amistad).filter(
            Amistad.estado == 'pendiente',
            Amistad.amigo_id == usuario_id,
        ).all()

    @staticmethod
    def fetch_amigos_usuarios(db: Session, usuario_id: int) -> List["Usuario"]:
        """Devuelve los objetos Usuario que son amigos aceptados del usuario.

        Resuelve el "otro lado" de cada amistad aceptada (sea quien haya enviado
        la solicitud) para poder mostrar nombre/avatar en el frontend.
        """
        from Modelo.Usuario import Usuario

        amistades = AmistadRepo.fetch_amigos(db, usuario_id)
        ids_amigos = []
        for a in amistades:
            otro = a.amigo_id if a.usuario_id == usuario_id else a.usuario_id
            if otro not in ids_amigos:
                ids_amigos.append(otro)
        if not ids_amigos:
            return []
        return db.query(Usuario).filter(Usuario.id.in_(ids_amigos)).all()

    @staticmethod
    def fetch_pendientes_solicitantes(db: Session, usuario_id: int):
        """Devuelve pares (amistad, usuario_solicitante) de solicitudes pendientes."""
        from Modelo.Usuario import Usuario

        pendientes = AmistadRepo.fetch_pendientes(db, usuario_id)
        resultado = []
        for a in pendientes:
            solicitante = db.query(Usuario).filter(Usuario.id == a.usuario_id).first()
            resultado.append((a, solicitante))
        return resultado

    @staticmethod
    def fetch_by_id(db: Session, amistad_id: int) -> Optional[Amistad]:
        return db.query(Amistad).filter(Amistad.id == amistad_id).first()

    @staticmethod
    def existe_amistad(db: Session, usuario_id: int, amigo_id: int) -> bool:
        return db.query(Amistad).filter(
            or_(
                and_(Amistad.usuario_id == usuario_id, Amistad.amigo_id == amigo_id),
                and_(Amistad.usuario_id == amigo_id, Amistad.amigo_id == usuario_id)
            )
        ).first() is not None

    @staticmethod
    def crear_con_validaciones(db: Session, amistad_data: dict) -> Amistad:
        usuario_id = amistad_data['usuario_id']
        amigo_id = amistad_data['amigo_id']

        if usuario_id == amigo_id:
            raise HTTPException(status_code=400, detail="No puedes ser tu propio amigo, compa.")

        if AmistadRepo.existe_amistad(db, usuario_id, amigo_id):
            raise HTTPException(status_code=400, detail="Ya existe una relación entre estos usuarios.")

        nueva = Amistad(**amistad_data)
        db.add(nueva)
        db.flush()

        # Notificar al destinatario de la solicitud de amistad.
        from Repositorio.Notificacion import NotificacionRepo
        from Modelo.Usuario import Usuario
        solicitante = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        nombre = solicitante.nombre if solicitante else "Alguien"
        NotificacionRepo.crear(
            db, amigo_id, "amistad",
            f"{nombre} te envió una solicitud de amistad.", ref_id=nueva.id
        )

        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def delete(db: Session, amistad_id: int) -> Type[Amistad] | None:
        orden = db.query(Amistad).filter(Amistad.id == amistad_id).first()
        if orden:
            db.delete(orden)
            db.commit()
            return orden
        return None

    @staticmethod
    def update(db: Session, amistad_id: int, amistad_data: dict) -> Optional[Amistad]:
        categoria = db.query(Amistad).filter(Amistad.id == amistad_id).first()
        if categoria:
            for key, value in amistad_data.items():
                setattr(categoria, key, value)
            db.commit()
            db.refresh(categoria)
            return categoria
        return None
