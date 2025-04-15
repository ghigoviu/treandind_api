from pydantic import BaseModel
from typing import Optional


class ProductoImagenBase(BaseModel):
    url: str
    es_portada: bool = False


class ProductoImagenCreate(ProductoImagenBase):
    producto_id: int


class ProductoImagenRead(ProductoImagenBase):
    id: int

    class Config:
        orm_mode = True
