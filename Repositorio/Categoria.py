from sqlalchemy.orm import Session
from Modelo.Categoria import Categoria
from typing import Optional, List


class CategoriaRepo:

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> List[Categoria]:
        return db.query(Categoria).offset(skip).limit(limit).all()

    @staticmethod
    def fetch_by_id(db: Session, categoria_id: int) -> Optional[Categoria]:
        return db.query(Categoria).filter(Categoria.id == categoria_id).first()

    @staticmethod
    def create(db: Session, categoria_data: dict) -> Categoria:
        nueva = Categoria(**categoria_data)
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def update(db: Session, categoria_id: int, categoria_data: dict) -> Optional[Categoria]:
        categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if categoria:
            for key, value in categoria_data.items():
                setattr(categoria, key, value)
            db.commit()
            db.refresh(categoria)
            return categoria
        return None

    @staticmethod
    def delete(db: Session, categoria_id: int) -> Optional[Categoria]:
        categoria = db.query(Categoria).filter(Categoria.id == categoria_id).first()
        if categoria:
            db.delete(categoria)
            db.commit()
            return categoria
        return None
