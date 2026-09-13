from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List

from Schema.Colaboracion import (
    ColaboracionCreate, ColaboracionUpdate, ColaboracionRead,
    InvitarMiembro, ResponderInvitacion,
)
from Repositorio.Colaboracion import ColaboracionRepo
from ControladorRest import get_db


class ColaboracionRest:
    router = APIRouter(prefix="/colaboracion", tags=["Colaboraciones"])

    @router.get("/", response_model=List[ColaboracionRead])
    def obtener_todas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return ColaboracionRepo.fetch_all(db, skip, limit)

    @router.get("/{colaboracion_id}", response_model=ColaboracionRead)
    def obtener_por_id(colaboracion_id: int, db: Session = Depends(get_db)):
        colaboracion = ColaboracionRepo.fetch_by_id(db, colaboracion_id)
        if not colaboracion:
            raise HTTPException(status_code=404, detail="Colaboración no encontrada")
        return colaboracion

    @router.get("/usuario/{usuario_id}", response_model=List[ColaboracionRead])
    def obtener_por_usuario(usuario_id: int, db: Session = Depends(get_db)):
        return ColaboracionRepo.fetch_by_usuario(db, usuario_id)

    @router.get("/{colaboracion_id}/detalle")
    def obtener_detalle(colaboracion_id: int, db: Session = Depends(get_db)):
        """Colaboración con creador y miembros enriquecidos para el frontend."""
        detalle = ColaboracionRepo.fetch_detalle(db, colaboracion_id)
        if not detalle:
            raise HTTPException(status_code=404, detail="Colaboración no encontrada")
        return detalle

    @router.post("/", response_model=ColaboracionRead, status_code=status.HTTP_201_CREATED)
    def crear(colaboracion: ColaboracionCreate, db: Session = Depends(get_db)):
        return ColaboracionRepo.create(db, colaboracion.dict())

    @router.put("/{colaboracion_id}", response_model=ColaboracionRead)
    def actualizar(colaboracion_id: int, colaboracion: ColaboracionUpdate, db: Session = Depends(get_db)):
        actualizada = ColaboracionRepo.update(db, colaboracion_id, colaboracion.dict(exclude_unset=True))
        if not actualizada:
            raise HTTPException(status_code=404, detail="Colaboración no encontrada")
        return actualizada

    @router.delete("/{colaboracion_id}")
    def eliminar(colaboracion_id: int, db: Session = Depends(get_db)):
        eliminada = ColaboracionRepo.delete(db, colaboracion_id)
        if not eliminada:
            raise HTTPException(status_code=404, detail="Colaboración no encontrada")
        return {"mensaje": "Colaboración eliminada", "id": eliminada["id"]}

    @router.post("/{colaboracion_id}/invitar", status_code=status.HTTP_201_CREATED)
    def invitar(colaboracion_id: int, body: InvitarMiembro, db: Session = Depends(get_db)):
        """Invita a un amigo a colaborar con un porcentaje sugerido."""
        miembro = ColaboracionRepo.invitar(db, colaboracion_id, body.usuario_id, body.porcentaje_sugerido)
        return {
            "mensaje": "Invitación enviada",
            "colaboracion_id": colaboracion_id,
            "usuario_id": miembro.usuario_id,
            "porcentaje_sugerido": miembro.porcentaje_sugerido,
            "estado": miembro.estado,
        }

    @router.post("/{colaboracion_id}/responder/{usuario_id}")
    def responder(colaboracion_id: int, usuario_id: int, body: ResponderInvitacion, db: Session = Depends(get_db)):
        """El invitado acepta el % sugerido o replica con su propio %."""
        miembro = ColaboracionRepo.responder_invitacion(
            db, colaboracion_id, usuario_id, body.accion, body.porcentaje
        )
        return {
            "mensaje": "Respuesta registrada",
            "estado": miembro.estado,
            "porcentaje": miembro.porcentaje,
        }

    @router.get("/{colaboracion_id}/puede-publicar")
    def puede_publicar(colaboracion_id: int, db: Session = Depends(get_db)):
        return {"puede_publicar": ColaboracionRepo.puede_publicar(db, colaboracion_id)}
