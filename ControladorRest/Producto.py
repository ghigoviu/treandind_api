from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Repositorio.Producto import ProductoRepo
from Schema.Producto import ProductoCreate, ProductoRead, ProductoUpdate, ProductoSchema
from ControladorRest import get_db


class ProductoRest:
    router = APIRouter(prefix="/productos", tags=["Productos"])

    @router.post("/", response_model=ProductoRead)
    def create(producto: ProductoCreate, db: Session = Depends(get_db)):
        return ProductoRepo.create(db, producto)

    @router.get("/", response_model=List[ProductoRead])
    def get_all(db: Session = Depends(get_db)):
        return ProductoRepo.fetch_all(db)

    @router.get("/id/{producto_id}", response_model=ProductoSchema)
    def get_by_id(producto_id: int, db: Session = Depends(get_db)):
        db_producto = ProductoRepo.fetch_by_id(db, producto_id)
        if not db_producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return db_producto

    @router.put("/{producto_id}", response_model=ProductoRead)
    def update(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
        db_producto = ProductoRepo.update(db, producto_id, producto.dict())
        if not db_producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return db_producto

    @router.delete("/{producto_id}", response_model=ProductoRead)
    def delete(producto_id: int, db: Session = Depends(get_db)):
        db_producto = ProductoRepo.delete(db, producto_id)
        if not db_producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return db_producto
