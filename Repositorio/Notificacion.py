from sqlalchemy.orm import Session
from typing import List, Optional

from Modelo.Notificacion import Notificacion


class NotificacionRepo:

    @staticmethod
    def crear(db: Session, usuario_id: int, tipo: str, mensaje: str, ref_id: Optional[int] = None) -> Notificacion:
        """Crea una notificación SIN commit. Pensado para usarse dentro de la
        transacción del evento que la origina (venta, amistad, etc.)."""
        notif = Notificacion(usuario_id=usuario_id, tipo=tipo, mensaje=mensaje, ref_id=ref_id)
        db.add(notif)
        return notif

    @staticmethod
    def crear_y_guardar(db: Session, usuario_id: int, tipo: str, mensaje: str, ref_id: Optional[int] = None) -> Notificacion:
        """Crea una notificación y hace commit (uso standalone)."""
        notif = NotificacionRepo.crear(db, usuario_id, tipo, mensaje, ref_id)
        db.commit()
        db.refresh(notif)
        return notif

    @staticmethod
    def fetch_by_usuario(db: Session, usuario_id: int, solo_no_leidas: bool = False) -> List[Notificacion]:
        q = db.query(Notificacion).filter(Notificacion.usuario_id == usuario_id)
        if solo_no_leidas:
            q = q.filter(Notificacion.leida == False)
        return q.order_by(Notificacion.creado_en.desc()).all()

    @staticmethod
    def contar_no_leidas(db: Session, usuario_id: int) -> int:
        return db.query(Notificacion).filter(
            Notificacion.usuario_id == usuario_id,
            Notificacion.leida == False,
        ).count()

    @staticmethod
    def marcar_leida(db: Session, notificacion_id: int) -> Optional[Notificacion]:
        notif = db.query(Notificacion).filter(Notificacion.id == notificacion_id).first()
        if not notif:
            return None
        notif.leida = True
        db.commit()
        db.refresh(notif)
        return notif

    @staticmethod
    def marcar_todas_leidas(db: Session, usuario_id: int) -> int:
        n = db.query(Notificacion).filter(
            Notificacion.usuario_id == usuario_id,
            Notificacion.leida == False,
        ).update({Notificacion.leida: True})
        db.commit()
        return n
