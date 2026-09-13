from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Schema.Seguidor import SeguidorCreate, SeguidorRead, SeguidorDetalle
from Schema.Base.Usuario import UsuarioRead
from Repositorio.Seguidor import SeguidorRepo
from ControladorRest import get_db


class SeguidorRest:
    router = APIRouter(prefix="/seguidores", tags=["Seguidores"])

    @router.post("/", response_model=SeguidorRead, status_code=201)
    def seguir(body: SeguidorCreate, db: Session = Depends(get_db)):
        return SeguidorRepo.seguir(db, body.seguidor_id, body.seguido_id)

    @router.delete("/")
    def dejar_de_seguir(seguidor_id: int, seguido_id: int, db: Session = Depends(get_db)):
        ok = SeguidorRepo.dejar_de_seguir(db, seguidor_id, seguido_id)
        if not ok:
            raise HTTPException(status_code=404, detail="No sigues a este usuario.")
        return {"mensaje": "Dejaste de seguir al usuario."}

    @router.get("/usuario/{usuario_id}/siguiendo", response_model=List[UsuarioRead])
    def get_siguiendo(usuario_id: int, db: Session = Depends(get_db)):
        """Usuarios a los que sigue (con datos)."""
        return SeguidorRepo.fetch_siguiendo(db, usuario_id)

    @router.get("/usuario/{usuario_id}/seguidores", response_model=List[UsuarioRead])
    def get_seguidores(usuario_id: int, db: Session = Depends(get_db)):
        """Usuarios que siguen a este usuario."""
        return SeguidorRepo.fetch_seguidores(db, usuario_id)

    @router.get("/usuario/{usuario_id}/contadores")
    def get_contadores(usuario_id: int, db: Session = Depends(get_db)):
        return {
            "siguiendo": SeguidorRepo.contar_siguiendo(db, usuario_id),
            "seguidores": SeguidorRepo.contar_seguidores(db, usuario_id),
        }

    @router.get("/usuario/{seguidor_id}/sigue/{seguido_id}")
    def check_sigue(seguidor_id: int, seguido_id: int, db: Session = Depends(get_db)):
        return {"sigue": SeguidorRepo.esta_siguiendo(db, seguidor_id, seguido_id)}
