from pydantic import BaseModel
from typing import Optional


class OrdenDetalleBase(BaseModel):
    cantidad: int
    precio_unit: float


class OrdenDetalleCreate(OrdenDetalleBase):
    orden_id: int
    producto_id: Optional[int] = None
    evento_id: Optional[int] = None


class OrdenDetalleRead(OrdenDetalleBase):
    id: int

    class Config:
        from_attributes = True
