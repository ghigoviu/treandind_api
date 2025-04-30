from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from Repositorio.Compartido import CompartidoRepo
from Schema.Compartido import CompartidoUpdate, CompartidoRead, CompartidoCreate
from ControladorRest import get_db


class CompartidoRest:
    router = APIRouter(prefix="/compartidos", tags=["Compartidos"])

    @router.get("/", response_model=List[CompartidoRead])
    def obtener_todos(db: Session = Depends(get_db)):
        return CompartidoRepo.fetch_all(db)

    @router.get("/{compartido_id}", response_model=CompartidoRead)
    def obtener_por_id(compartido_id: int, db: Session = Depends(get_db)):
        compartido = CompartidoRepo.fetch_by_id(db, compartido_id)
        if not compartido:
            raise HTTPException(status_code=404, detail="Compartido no encontrado")
        return compartido

    @router.post("/", response_model=CompartidoRead, status_code=status.HTTP_201_CREATED)
    def crear_compartido(payload: CompartidoCreate, db: Session = Depends(get_db)):
        return CompartidoRepo.create(db, payload.dict())

    @router.put("/{compartido_id}", response_model=CompartidoRead)
    def actualizar_compartido(compartido_id: int, payload: CompartidoUpdate, db: Session = Depends(get_db)):
        compartido = CompartidoRepo.update(db, compartido_id, payload.dict(exclude_unset=True))
        if not compartido:
            raise HTTPException(status_code=404, detail="Compartido no encontrado")
        return compartido
