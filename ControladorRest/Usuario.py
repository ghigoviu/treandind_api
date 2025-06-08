from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from Schema.Base.Usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate, LoginRequest
from Schema.Usuario import UsuarioSchema
from Repositorio.Usuario import UsuarioRepo
from ControladorRest import get_db


class UsuarioRest:
    router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

    @router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
    def crear(usuario: UsuarioCreate, db: Session = Depends(get_db)):
        if UsuarioRepo.fetch_by_email(db, usuario.email):
            raise HTTPException(status_code=400, detail="El email ya está registrado.")
        usuario_creado = UsuarioRepo.create(db, usuario.dict())
        return usuario_creado

    @router.get("/", response_model=List[UsuarioRead])
    def obtener_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return UsuarioRepo.fetch_all(db, skip=skip, limit=limit)

    @router.post("/login", response_model=UsuarioSchema)
    def login(request: LoginRequest, db: Session = Depends(get_db)):
        usuario = UsuarioRepo.fetch_by_email(db, request.email)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

        if usuario.password != request.password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

        return usuario

    @router.get("/id/{usuario_id}", response_model=UsuarioSchema)
    def obtener_por_id(usuario_id: int, db: Session = Depends(get_db)):
        usuario = UsuarioRepo.fetch_by_id(db, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

    @router.put("/{usuario_id}", response_model=UsuarioRead)
    def actualizar(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
        actualizado = UsuarioRepo.update(db, usuario_id, usuario.dict(exclude_unset=True))
        if not actualizado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return actualizado

    @router.delete("/{usuario_id}", response_model=UsuarioRead)
    def eliminar(usuario_id: int, db: Session = Depends(get_db)):
        eliminado = UsuarioRepo.delete(db, usuario_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return eliminado
