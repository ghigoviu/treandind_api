from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class OrdenDetalleCreate(BaseModel):
    producto_id: Optional[int] = None
    evento_id: Optional[int] = None
    cantidad: int = Field(..., gt=0)
    precio_unitario: float = Field(..., gt=0)

    @field_validator
    def validate_one_fk(cls, values):
        producto_id, evento_id = values.get("producto_id"), values.get("evento_id")
        if not producto_id and not evento_id:
            raise ValueError("Debe incluir al menos un producto_id o evento_id.")
        if producto_id and evento_id:
            raise ValueError("Solo se debe especificar producto_id o evento_id, no ambos.")
        return values


class OrdenBase(BaseModel):
    estado: str
    total: float = Field(..., gt=0)
    usuario_id: int


class OrdenCreate(BaseModel):
    orden: OrdenBase
    detalles: List[OrdenDetalleCreate]


class OrdenRead(BaseModel):
    id: int
    estado: str
    total: float
    creado_en: datetime
    usuario_id: int

    class Config:
        orm_mode = True


class OrdenDetalleRead(BaseModel):
    id: int
    producto_id: Optional[int]
    evento_id: Optional[int]
    cantidad: int
    precio_unitario: float

    class Config:
        orm_mode = True
