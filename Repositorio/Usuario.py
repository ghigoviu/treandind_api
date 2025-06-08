from sqlalchemy.orm import Session
from Modelo.Usuario import Usuario
from typing import Optional, Type


class UsuarioRepo:
    @staticmethod
    def fetch_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    @staticmethod
    def fetch_by_email(db: Session, email: str) -> Optional[Usuario]:
        return db.query(Usuario).filter(Usuario.email == email).first()

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Usuario]]:
        return db.query(Usuario).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, usuario_data: dict) -> Usuario:
        usuario = Usuario(**usuario_data)
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def update(db: Session, usuario_id: int, usuario_data: dict) -> Type[Usuario] | None:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if usuario:
            for key, value in usuario_data.items():
                if hasattr(usuario, key):
                    setattr(usuario, key, value)
            db.commit()
            db.refresh(usuario)
            print(usuario)
            return usuario
        return None

    @staticmethod
    def delete(db: Session, usuario_id: int) -> Optional[Usuario]:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if usuario:
            db.delete(usuario)
            db.commit()
            return usuario
        return None
