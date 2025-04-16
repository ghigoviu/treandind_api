from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from Schema.Amistad import AmistadRead, AmistadCreate, AmistadUpdate
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

    @router.get("/{amistad_id}", response_model=AmistadRead)
    def obtener_por_id(amistad_id: int, db: Session = Depends(get_db)):
        amistad = AmistadRepo.fetch_by_id(db, amistad_id)
        if not amistad:
            raise HTTPException(status_code=404, detail="Amistad no encontrada")
        return amistad

    @router.put("/{amistad_id}", response_model=AmistadRead)
    def actualizar(amistad_id: int, amistad: AmistadUpdate, db: Session = Depends(get_db)):
        actualizada = AmistadRepo.update(db, amistad_id, amistad.dict(exclude_unset=True))
        if not actualizada:
            raise HTTPException(status_code=404, detail="Amistad no encontrada")
        return actualizada

    @router.delete("/{amistad_id}", response_model=AmistadRead)
    def eliminar(amistad_id: int, db: Session = Depends(get_db)):
        eliminada = AmistadRepo.delete(db, amistad_id)
        if not eliminada:
            raise HTTPException(status_code=404, detail="Amistad no encontrada")
        return eliminada
