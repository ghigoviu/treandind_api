from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from Modelo.Paquete import Paquete
from Modelo.SuscripcionMembresia import SuscripcionMembresia
from Modelo.Usuario import Usuario

# Días que dura cada frecuencia de membresía.
DIAS_FRECUENCIA = {"mensual": 30, "semestral": 182, "anual": 365}


class MembresiaRepo:

    # --- Paquetes ------------------------------------------------------------

    @staticmethod
    def crear_paquete(db: Session, data: dict) -> Paquete:
        vendedor = db.query(Usuario).filter(Usuario.id == data.get("vendedor_id")).first()
        if not vendedor:
            raise HTTPException(status_code=404, detail="Vendedor no encontrado.")
        if vendedor.tipo_perfil not in ('vendedor', 'influencer'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo vendedores o influencers pueden crear paquetes de membresía."
            )
        paquete = Paquete(**data)
        db.add(paquete)
        db.commit()
        db.refresh(paquete)
        return paquete

    @staticmethod
    def fetch_paquetes_por_vendedor(db: Session, vendedor_id: int) -> List[Paquete]:
        return db.query(Paquete).filter(Paquete.vendedor_id == vendedor_id).all()

    # --- Suscripciones -------------------------------------------------------

    @staticmethod
    def suscribir(db: Session, usuario_id: int, paquete_id: int) -> SuscripcionMembresia:
        paquete = db.query(Paquete).filter(Paquete.id == paquete_id).first()
        if not paquete:
            raise HTTPException(status_code=404, detail="Paquete no encontrado.")

        # Vencimiento según la frecuencia del paquete.
        dias = DIAS_FRECUENCIA.get(paquete.frecuencia, 30)
        vencimiento = datetime.now() + timedelta(days=dias)

        suscripcion = SuscripcionMembresia(
            usuario_id=usuario_id,
            paquete_id=paquete_id,
            vendedor_id=paquete.vendedor_id,
            vencimiento=vencimiento,
            estado='activa',
        )
        db.add(suscripcion)
        db.commit()
        db.refresh(suscripcion)
        return suscripcion

    @staticmethod
    def suscripcion_activa(db: Session, usuario_id: int, vendedor_id: int) -> bool:
        """True si el usuario tiene una suscripción activa y no vencida con el vendedor."""
        ahora = datetime.now()
        sus = (
            db.query(SuscripcionMembresia)
            .filter(
                SuscripcionMembresia.usuario_id == usuario_id,
                SuscripcionMembresia.vendedor_id == vendedor_id,
                SuscripcionMembresia.estado == 'activa',
                SuscripcionMembresia.vencimiento > ahora,
            )
            .first()
        )
        return sus is not None

    @staticmethod
    def fetch_suscripciones_usuario(db: Session, usuario_id: int) -> List[SuscripcionMembresia]:
        return db.query(SuscripcionMembresia).filter(
            SuscripcionMembresia.usuario_id == usuario_id
        ).all()

    @staticmethod
    def procesar_vencimientos(db: Session, dias_alerta: int = 7) -> dict:
        """Marca como 'vencida' las suscripciones caducadas y genera alertas
        (notificaciones) para las próximas a vencer. Devuelve conteos."""
        from Repositorio.Notificacion import NotificacionRepo

        ahora = datetime.now()
        limite_alerta = ahora + timedelta(days=dias_alerta)

        # 1) Marcar vencidas.
        vencidas = (
            db.query(SuscripcionMembresia)
            .filter(
                SuscripcionMembresia.estado == 'activa',
                SuscripcionMembresia.vencimiento <= ahora,
            )
            .all()
        )
        for s in vencidas:
            s.estado = 'vencida'
            NotificacionRepo.crear(
                db, s.usuario_id, "membresia",
                "Tu membresía ha vencido.", ref_id=s.paquete_id
            )
            NotificacionRepo.crear(
                db, s.vendedor_id, "membresia",
                "La membresía de un suscriptor ha vencido.", ref_id=s.id
            )

        # 2) Alertar próximas a vencer (aún activas).
        por_vencer = (
            db.query(SuscripcionMembresia)
            .filter(
                SuscripcionMembresia.estado == 'activa',
                SuscripcionMembresia.vencimiento > ahora,
                SuscripcionMembresia.vencimiento <= limite_alerta,
            )
            .all()
        )
        for s in por_vencer:
            NotificacionRepo.crear(
                db, s.usuario_id, "membresia",
                "Tu membresía está por vencer pronto.", ref_id=s.paquete_id
            )

        db.commit()
        return {"vencidas": len(vencidas), "por_vencer": len(por_vencer)}
