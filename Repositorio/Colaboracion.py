from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional

from Modelo.ColaboracionUsuario import ColaboracionUsuario
from Modelo.Colaboracion import Colaboracion


class ColaboracionRepo:

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> List[Colaboracion]:
        return db.query(Colaboracion).offset(skip).limit(limit).all()

    @staticmethod
    def fetch_by_id(db: Session, colaboracion_id: int) -> Optional[Colaboracion]:
        return (
            db.query(Colaboracion)
            .options(joinedload(Colaboracion.usuarios))
            .filter(Colaboracion.id == colaboracion_id)
            .first()
        )

    @staticmethod
    def fetch_by_usuario(db: Session, usuario_id: int) -> List[Colaboracion]:
        """Colaboraciones en las que el usuario participa (como miembro)."""
        return (
            db.query(Colaboracion)
            .join(ColaboracionUsuario, ColaboracionUsuario.colaboracion_id == Colaboracion.id)
            .filter(ColaboracionUsuario.usuario_id == usuario_id)
            .all()
        )

    @staticmethod
    def create(db: Session, colaboracion_data: dict) -> Colaboracion:
        from Modelo.Usuario import Usuario

        # Solo un vendedor o influencer puede crear una página social.
        creador = db.query(Usuario).filter(Usuario.id == colaboracion_data.get("usuario_id")).first()
        if not creador:
            raise HTTPException(status_code=404, detail="Usuario creador no encontrado.")
        if creador.tipo_perfil not in ('vendedor', 'influencer'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un vendedor o influencer puede crear una página social."
            )

        try:
            colaboracion = Colaboracion(**colaboracion_data)
            db.add(colaboracion)
            db.flush()

            # El creador queda como miembro aceptado automáticamente.
            miembro_creador = ColaboracionUsuario(
                usuario_id=creador.id,
                colaboracion_id=colaboracion.id,
                porcentaje=0,
                estado='aceptada',
            )
            db.add(miembro_creador)

            db.commit()
            db.refresh(colaboracion)
            return colaboracion
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear la colaboración (datos inválidos o usuario inexistente)."
            )

    @staticmethod
    def update(db: Session, colaboracion_id: int, colaboracion_data: dict) -> Optional[Colaboracion]:
        colaboracion = db.query(Colaboracion).filter(Colaboracion.id == colaboracion_id).first()
        if not colaboracion:
            return None
        try:
            for key, value in colaboracion_data.items():
                setattr(colaboracion, key, value)
            db.commit()
            db.refresh(colaboracion)
            return colaboracion
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo actualizar la colaboración."
            )

    @staticmethod
    def delete(db: Session, colaboracion_id: int) -> Optional[dict]:
        colaboracion = db.query(Colaboracion).filter(Colaboracion.id == colaboracion_id).first()
        if not colaboracion:
            return None
        # Capturar datos antes de borrar (evita objeto detached en la respuesta).
        snapshot = {
            "id": colaboracion.id,
            "desc": colaboracion.desc,
            "nombre_comercial": colaboracion.nombre_comercial,
            "img": colaboracion.img,
            "video": colaboracion.video,
            "usuario_id": colaboracion.usuario_id,
            "creado_en": colaboracion.creado_en,
        }
        # Borrar miembros primero para no violar la FK.
        db.query(ColaboracionUsuario).filter(
            ColaboracionUsuario.colaboracion_id == colaboracion_id
        ).delete()
        db.delete(colaboracion)
        db.commit()
        return snapshot

    @staticmethod
    def fetch_detalle(db: Session, colaboracion_id: int) -> Optional[dict]:
        """Colaboración con creador y miembros enriquecidos (nombre/avatar)."""
        from Modelo.Usuario import Usuario

        colaboracion = ColaboracionRepo.fetch_by_id(db, colaboracion_id)
        if not colaboracion:
            return None

        creador = db.query(Usuario).filter(Usuario.id == colaboracion.usuario_id).first()

        miembros = []
        for cu in colaboracion.usuarios:
            u = db.query(Usuario).filter(Usuario.id == cu.usuario_id).first()
            miembros.append({
                "usuario_id": cu.usuario_id,
                "porcentaje": cu.porcentaje,
                "porcentaje_sugerido": cu.porcentaje_sugerido,
                "estado": cu.estado,
                "nombre": u.nombre if u else "Usuario",
                "imagen_perfil": u.imagen_perfil if u else None,
            })

        return {
            "id": colaboracion.id,
            "nombre_comercial": colaboracion.nombre_comercial,
            "desc": colaboracion.desc,
            "img": colaboracion.img,
            "video": colaboracion.video,
            "creado_en": colaboracion.creado_en,
            "puede_publicar": ColaboracionRepo.puede_publicar(db, colaboracion.id),
            "creador": {
                "id": creador.id if creador else None,
                "nombre": creador.nombre if creador else "Usuario",
                "imagen_perfil": creador.imagen_perfil if creador else None,
            } if creador else None,
            "miembros": miembros,
        }

    @staticmethod
    def invitar(db: Session, colaboracion_id: int, usuario_id: int, porcentaje_sugerido: int = 0) -> ColaboracionUsuario:
        """Invita a un usuario a la página social con un % sugerido. Crea el
        miembro en estado 'pendiente' y notifica al invitado."""
        from Modelo.Usuario import Usuario
        from Repositorio.Notificacion import NotificacionRepo

        colaboracion = db.query(Colaboracion).filter(Colaboracion.id == colaboracion_id).first()
        if not colaboracion:
            raise HTTPException(status_code=404, detail="Colaboración no encontrada")

        existe = (
            db.query(ColaboracionUsuario)
            .filter(
                ColaboracionUsuario.colaboracion_id == colaboracion_id,
                ColaboracionUsuario.usuario_id == usuario_id,
            )
            .first()
        )
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya forma parte de esta colaboración."
            )

        try:
            miembro = ColaboracionUsuario(
                usuario_id=usuario_id,
                colaboracion_id=colaboracion_id,
                porcentaje=0,
                porcentaje_sugerido=porcentaje_sugerido,
                estado='pendiente',
            )
            db.add(miembro)
            db.flush()

            nombre_pagina = colaboracion.nombre_comercial or "una página social"
            NotificacionRepo.crear(
                db, usuario_id, "invitacion",
                f"Te invitaron a colaborar en '{nombre_pagina}' con un {porcentaje_sugerido}% sugerido.",
                ref_id=colaboracion_id
            )

            db.commit()
            db.refresh(miembro)
            return miembro
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo invitar al miembro (usuario inexistente)."
            )

    @staticmethod
    def responder_invitacion(db: Session, colaboracion_id: int, usuario_id: int, accion: str, porcentaje: Optional[int] = None) -> ColaboracionUsuario:
        """El invitado acepta el % sugerido o replica proponiendo su propio %."""
        miembro = (
            db.query(ColaboracionUsuario)
            .filter(
                ColaboracionUsuario.colaboracion_id == colaboracion_id,
                ColaboracionUsuario.usuario_id == usuario_id,
            )
            .first()
        )
        if not miembro:
            raise HTTPException(status_code=404, detail="Invitación no encontrada")
        if miembro.estado != 'pendiente':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Esta invitación ya fue '{miembro.estado}'."
            )

        if accion == 'aceptar':
            miembro.porcentaje = miembro.porcentaje_sugerido
            miembro.estado = 'aceptada'
        elif accion == 'replicar':
            if porcentaje is None:
                raise HTTPException(status_code=400, detail="Debes indicar el porcentaje al replicar.")
            miembro.porcentaje = porcentaje
            miembro.estado = 'replicada'
        else:
            raise HTTPException(status_code=400, detail="Acción inválida (usa 'aceptar' o 'replicar').")

        db.commit()
        db.refresh(miembro)
        return miembro

    @staticmethod
    def puede_publicar(db: Session, colaboracion_id: int) -> bool:
        """La página puede publicar cuando TODOS los miembros aceptaron/replicaron
        (ninguno queda en estado 'pendiente')."""
        pendientes = (
            db.query(ColaboracionUsuario)
            .filter(
                ColaboracionUsuario.colaboracion_id == colaboracion_id,
                ColaboracionUsuario.estado == 'pendiente',
            )
            .count()
        )
        return pendientes == 0
