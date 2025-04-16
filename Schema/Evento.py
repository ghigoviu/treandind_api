from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None
    categoria: str
    fecha: datetime
    ubicacion: str
    img_evento: Optional[str] = None
    calificacion: Optional[float] = 0.0


class EventoCreate(EventoBase):
    usuario_id: int


class EventoRead(EventoBase):
    id: int
    creado_en: datetime

    class Config:
        from_attributes = True
