from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional

from Modelo.PerfilVendedor import PerfilVendedor
from Modelo.Usuario import Usuario


class PerfilVendedorRepo:

    @staticmethod
    def fetch_by_usuario(db: Session, usuario_id: int) -> Optional[PerfilVendedor]:
        return db.query(PerfilVendedor).filter(
            PerfilVendedor.usuario_id == usuario_id
        ).first()

    @staticmethod
    def create(db: Session, data: dict) -> PerfilVendedor:
        usuario_id = data.get("usuario_id")

        # Solo vendedor o influencer puede crear perfil de vendedor.
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        if usuario.tipo_perfil not in ('vendedor', 'influencer'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo usuarios con perfil vendedor o influencer pueden validarse."
            )

        existente = PerfilVendedorRepo.fetch_by_usuario(db, usuario_id)
        if existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un perfil de vendedor para este usuario."
            )

        try:
            perfil = PerfilVendedor(**data)
            # Auto-validar si todos los campos obligatorios están completos.
            perfil.validado = PerfilVendedorRepo._campos_completos(perfil)
            db.add(perfil)
            db.commit()
            db.refresh(perfil)
            return perfil
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear el perfil de vendedor."
            )

    @staticmethod
    def update(db: Session, usuario_id: int, data: dict) -> Optional[PerfilVendedor]:
        perfil = PerfilVendedorRepo.fetch_by_usuario(db, usuario_id)
        if not perfil:
            return None
        for key, value in data.items():
            if hasattr(perfil, key) and value is not None:
                setattr(perfil, key, value)
        # Recalcular validación.
        perfil.validado = PerfilVendedorRepo._campos_completos(perfil)
        db.commit()
        db.refresh(perfil)
        return perfil

    @staticmethod
    def esta_validado(db: Session, usuario_id: int) -> bool:
        """Shortcut para verificar si un usuario está validado como vendedor."""
        perfil = PerfilVendedorRepo.fetch_by_usuario(db, usuario_id)
        return perfil is not None and perfil.validado

    @staticmethod
    def _campos_completos(perfil: PerfilVendedor) -> bool:
        """Retorna True si los 4 campos obligatorios están completos."""
        return all([
            perfil.metodos_entrega and perfil.metodos_entrega.strip(),
            perfil.lugares_entrega and perfil.lugares_entrega.strip(),
            perfil.info_general and perfil.info_general.strip(),
            perfil.datos_bancarios and perfil.datos_bancarios.strip(),
        ])
