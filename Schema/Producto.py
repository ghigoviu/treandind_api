from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int
    categoria_id: Optional[int] = None
    requiere_edad: bool = False


class ProductoCreate(ProductoBase):
    usuario_id: int


class ProductoRead(ProductoBase):
    id: int
    calificacion: float
    creado_en: datetime

    class Config:
        from_attributes = True


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    categoria_id: Optional[int] = None
    requiere_edad: Optional[bool] = None
