from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from Schema.Producto import ProductoCreate, ProductoRead, ProductoUpdate
from Repositorio.Producto import ProductoRepo
from ControladorRest import get_db


class ProductoRest:
    router = APIRouter(prefix="/productos", tags=["Productos"])

    @router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
    def crear(producto: ProductoCreate, db: Session = Depends(get_db)):
        return ProductoRepo.create_con_validaciones(db, producto.dict())

    @router.get("/", response_model=List[ProductoRead])
    def obtener_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return ProductoRepo.fetch_all(db, skip, limit)

    @router.get("/{producto_id}", response_model=ProductoRead)
    def obtener_por_id(producto_id: int, db: Session = Depends(get_db)):
        producto = ProductoRepo.fetch_by_id(db, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado.")
        return producto

    @router.put("/{producto_id}", response_model=ProductoRead)
    def actualizar(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
        return ProductoRepo.update_con_validaciones(db, producto_id, producto.dict(exclude_unset=True))

    @router.delete("/{producto_id}", response_model=ProductoRead)
    def eliminar(producto_id: int, db: Session = Depends(get_db)):
        producto = ProductoRepo.delete(db, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado.")
        return producto
