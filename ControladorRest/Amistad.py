from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List

from Modelo.Amistad import Amistad
from Schema.Amistad import AmistadRead, AmistadCreate, AmistadUpdate
from Schema.Base.Usuario import UsuarioRead
from Repositorio.Amistad import AmistadRepo
from ControladorRest import get_db


class AmistadRest:
    router = APIRouter(prefix="/amistades", tags=["Amistades"])

    @router.post("/", response_model=AmistadRead, status_code=status.HTTP_201_CREATED)
    def crear(amistad: AmistadCreate, db: Session = Depends(get_db)):
        return AmistadRepo.crear_con_validaciones(db, amistad.dict())

    @router.get("/", response_model=List[AmistadRead])
    def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return AmistadRepo.fetch_all(db, skip, limit)

    @router.get("/usuario/{usuario_id}", response_model=List[AmistadRead])
    def get_amigos(usuario_id: int, db: Session = Depends(get_db)):
        """Amistades aceptadas del usuario (en cualquier dirección)."""
        return AmistadRepo.fetch_amigos(db, usuario_id)

    @router.get("/usuario/{usuario_id}/pendientes", response_model=List[AmistadRead])
    def get_pendientes(usuario_id: int, db: Session = Depends(get_db)):
        """Solicitudes de amistad pendientes recibidas por el usuario."""
        return AmistadRepo.fetch_pendientes(db, usuario_id)

    @router.get("/usuario/{usuario_id}/detalle", response_model=List[UsuarioRead])
    def get_amigos_detalle(usuario_id: int, db: Session = Depends(get_db)):
        """Usuarios amigos (aceptados) con sus datos, listos para el frontend."""
        return AmistadRepo.fetch_amigos_usuarios(db, usuario_id)

    @router.get("/usuario/{usuario_id}/pendientes/detalle")
    def get_pendientes_detalle(usuario_id: int, db: Session = Depends(get_db)):
        """Solicitudes pendientes recibidas, con datos del solicitante."""
        pares = AmistadRepo.fetch_pendientes_solicitantes(db, usuario_id)
        salida = []
        for amistad, solicitante in pares:
            salida.append({
                "amistad_id": amistad.id,
                "estado": amistad.estado,
                "solicitante": {
                    "id": solicitante.id if solicitante else None,
                    "nombre": solicitante.nombre if solicitante else "Usuario",
                    "imagen_perfil": solicitante.imagen_perfil if solicitante else None,
                } if solicitante else None,
            })
        return salida

    @router.get("/{amistad_id}", response_model=AmistadRead)
    def obtener_por_id(amistad_id: int, db: Session = Depends(get_db)):
        amistad = AmistadRepo.fetch_by_id(db, amistad_id)
        if not amistad:
            raise HTTPException(status_code=404, detail="Amistad no encontrada")
        return amistad

    @router.patch("/{amistad_id}/estado")
    def actualizar_estado_amistad(amistad_id: int = Path(..., gt=0), datos: AmistadUpdate = None, db: Session = Depends(get_db)):
        from Repositorio.Seguidor import SeguidorRepo

        amistad = db.query(Amistad).filter(Amistad.id == amistad_id).first()
        if not amistad:
            raise HTTPException(status_code=404, detail="Amistad no encontrada")

        if amistad.estado != 'pendiente':
            raise HTTPException(
                status_code=400,
                detail=f"No se puede actualizar una amistad que ya fue '{amistad.estado}'"
            )

        amistad.estado = datos.estado

        # Al aceptar amistad, auto-seguir en ambos sentidos (requisito a.7).
        if datos.estado == 'aceptada':
            SeguidorRepo.seguir_silencioso(db, amistad.usuario_id, amistad.amigo_id)
            SeguidorRepo.seguir_silencioso(db, amistad.amigo_id, amistad.usuario_id)

        db.commit()
        db.refresh(amistad)

        return {"mensaje": "Estado actualizado correctamente", "amistad": amistad}

    @router.delete("/{amistad_id}", response_model=AmistadRead)
    def eliminar(amistad_id: int, db: Session = Depends(get_db)):
        eliminada = AmistadRepo.delete(db, amistad_id)
        if not eliminada:
            raise HTTPException(status_code=404, detail="Amistad no encontrada")
        return eliminada
