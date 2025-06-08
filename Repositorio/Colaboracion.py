from sqlalchemy.orm import Session, joinedload
from typing import List, Type

from Modelo.ColaboracionUsuario import ColaboracionUsuario
from Modelo.Colaboracion import Colaboracion


class ColaboracionRepo:

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> List[Colaboracion]:
        return db.query(Colaboracion).offset(skip).limit(limit).all()

    ## Recordar colocar una valdacion para evitar que el mismo usuario esté en la misma colaboracion

    '''
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
    '''

    def fetch_by_usuario(db: Session, usuario_id: int) -> List[Colaboracion]:
        return db.query(Colaboracion).where(ColaboracionUsuario.usuario_id == usuario_id).all()

    def fetch_by_id(db: Session, colaboracion_id: int) -> Type[Colaboracion] | None:
        return db.query(Colaboracion).options(joinedload(Colaboracion.usuarios)) \
                .filter(ColaboracionUsuario.colaboracion_id == colaboracion_id).first()
