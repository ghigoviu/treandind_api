from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from Schema.Categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from Repositorio.Categoria import CategoriaRepo
from ControladorRest import get_db


class CategoriaRest:
    router = APIRouter(prefix="/categorias", tags=["Categorías"])

    @router.get("/", response_model=List[CategoriaRead])
    def obtener_todas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return CategoriaRepo.fetch_all(db, skip, limit)

    @router.get("/{categoria_id}", response_model=CategoriaRead)
    def obtener_por_id(categoria_id: int, db: Session = Depends(get_db)):
        categoria = CategoriaRepo.fetch_by_id(db, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return categoria

    @router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
    def crear(categoria: CategoriaCreate, db: Session = Depends(get_db)):
        return CategoriaRepo.create(db, categoria.dict())

    @router.put("/{categoria_id}", response_model=CategoriaRead)
    def actualizar(categoria_id: int, categoria: CategoriaUpdate, db: Session = Depends(get_db)):
        actualizada = CategoriaRepo.update(db, categoria_id, categoria.dict(exclude_unset=True))
        if not actualizada:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return actualizada

    @router.delete("/{categoria_id}", response_model=CategoriaRead)
    def eliminar(categoria_id: int, db: Session = Depends(get_db)):
        eliminada = CategoriaRepo.delete(db, categoria_id)
        if not eliminada:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return eliminada
