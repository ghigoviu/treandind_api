from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Schema.Notificacion import NotificacionRead
from Repositorio.Notificacion import NotificacionRepo
from ControladorRest import get_db


class NotificacionRest:
    router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])

    @router.get("/usuario/{usuario_id}", response_model=List[NotificacionRead])
    def get_by_usuario(usuario_id: int, solo_no_leidas: bool = False, db: Session = Depends(get_db)):
        return NotificacionRepo.fetch_by_usuario(db, usuario_id, solo_no_leidas)

    @router.get("/usuario/{usuario_id}/contador")
    def contador(usuario_id: int, db: Session = Depends(get_db)):
        return {"no_leidas": NotificacionRepo.contar_no_leidas(db, usuario_id)}

    @router.patch("/{notificacion_id}/leida", response_model=NotificacionRead)
    def marcar_leida(notificacion_id: int, db: Session = Depends(get_db)):
        notif = NotificacionRepo.marcar_leida(db, notificacion_id)
        if not notif:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        return notif

    @router.patch("/usuario/{usuario_id}/leer-todas")
    def marcar_todas(usuario_id: int, db: Session = Depends(get_db)):
        n = NotificacionRepo.marcar_todas_leidas(db, usuario_id)
        return {"marcadas": n}
