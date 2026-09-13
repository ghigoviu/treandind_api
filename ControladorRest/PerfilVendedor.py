from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Schema.PerfilVendedor import PerfilVendedorCreate, PerfilVendedorUpdate, PerfilVendedorRead
from Repositorio.PerfilVendedor import PerfilVendedorRepo
from ControladorRest import get_db


class PerfilVendedorRest:
    router = APIRouter(prefix="/perfil-vendedor", tags=["Perfil Vendedor"])

    @router.post("/", response_model=PerfilVendedorRead, status_code=201)
    def crear(data: PerfilVendedorCreate, db: Session = Depends(get_db)):
        return PerfilVendedorRepo.create(db, data.dict())

    @router.get("/usuario/{usuario_id}", response_model=PerfilVendedorRead)
    def obtener(usuario_id: int, db: Session = Depends(get_db)):
        perfil = PerfilVendedorRepo.fetch_by_usuario(db, usuario_id)
        if not perfil:
            raise HTTPException(status_code=404, detail="Perfil de vendedor no encontrado.")
        return perfil

    @router.put("/usuario/{usuario_id}", response_model=PerfilVendedorRead)
    def actualizar(usuario_id: int, data: PerfilVendedorUpdate, db: Session = Depends(get_db)):
        perfil = PerfilVendedorRepo.update(db, usuario_id, data.dict(exclude_unset=True))
        if not perfil:
            raise HTTPException(status_code=404, detail="Perfil de vendedor no encontrado.")
        return perfil

    @router.get("/usuario/{usuario_id}/validado")
    def check_validado(usuario_id: int, db: Session = Depends(get_db)):
        return {"validado": PerfilVendedorRepo.esta_validado(db, usuario_id)}
