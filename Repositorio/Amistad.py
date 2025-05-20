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
