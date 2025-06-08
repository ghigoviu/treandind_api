from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from Schema.Colaboracion import ColaboracionCreate, ColaboracionUpdate, ColaboracionRead
from Repositorio.Colaboracion import ColaboracionRepo
from ControladorRest import get_db


class ColaboracionRest:
    router = APIRouter(prefix="/colaboracion", tags=["Categorías"])

    @router.get("/", response_model=List[ColaboracionRead])
    def obtener_todas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return ColaboracionRepo.fetch_all(db, skip, limit)

    @router.get("/{categoria_id}", response_model=ColaboracionRead)
    def obtener_por_id(categoria_id: int, db: Session = Depends(get_db)):
        categoria = ColaboracionRepo.fetch_by_id(db, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return categoria

    @router.post("/", response_model=ColaboracionRead, status_code=status.HTTP_201_CREATED)
    def crear(categoria: ColaboracionCreate, db: Session = Depends(get_db)):
        return ColaboracionRepo.create(db, categoria.dict())

    @router.put("/{categoria_id}", response_model=ColaboracionRead)
    def actualizar(categoria_id: int, categoria: ColaboracionUpdate, db: Session = Depends(get_db)):
        actualizada = ColaboracionRepo.update(db, categoria_id, categoria.dict(exclude_unset=True))
        if not actualizada:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return actualizada

    @router.delete("/{categoria_id}", response_model=ColaboracionRead)
    def eliminar(categoria_id: int, db: Session = Depends(get_db)):
        eliminada = ColaboracionRepo.delete(db, categoria_id)
        if not eliminada:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return eliminada
