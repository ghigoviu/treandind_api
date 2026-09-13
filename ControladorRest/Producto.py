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

    @router.get("/vendedor/{usuario_id}", response_model=List[ProductoRead])
    def get_by_vendedor(usuario_id: int, db: Session = Depends(get_db)):
        """Productos publicados por un vendedor (incluye ocultos, para el dueño)."""
        return ProductoRepo.fetch_by_vendedor(db, usuario_id, incluir_ocultos=True)

    @router.get("/feed/{usuario_id}", response_model=List[ProductoRead])
    def get_feed(usuario_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
        """Timeline: productos de los vendedores que el usuario sigue."""
        return ProductoRepo.fetch_feed(db, usuario_id, skip, limit)

    @router.get("/id/{producto_id}")
    def get_by_id(producto_id: int, db: Session = Depends(get_db)):
        db_producto = ProductoRepo.fetch_by_id_personalizado(db, producto_id)
        if not db_producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return db_producto

    @router.put("/{producto_id}", response_model=ProductoRead)
    def update(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
        db_producto = ProductoRepo.update(db, producto_id, producto.dict())
        if not db_producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return db_producto

    @router.delete("/{producto_id}")
    def delete(producto_id: int, db: Session = Depends(get_db)):
        eliminado_id = ProductoRepo.delete(db, producto_id)
        if not eliminado_id:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"mensaje": "Producto eliminado", "id": eliminado_id}
