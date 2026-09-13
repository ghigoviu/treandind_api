from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventoAsistenteBase(BaseModel):
    estado: Optional[str] = 'pendiente'  # confirmada, pendiente, cancelada


class EventoAsistenteCreate(BaseModel):
    usuario_id: int
    evento_id: Optional[int] = None  # se toma de la ruta; opcional en el body
    estado: Optional[str] = 'pendiente'


class EventoAsistenteRead(EventoAsistenteBase):
    id: int
    creado_en: datetime

    class Config:
        from_attributes = True
