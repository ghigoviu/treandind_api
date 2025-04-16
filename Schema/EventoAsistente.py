from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventoAsistenteBase(BaseModel):
    estado: str  # Ej: "confirmada", "pendiente", "cancelada"


class EventoAsistenteCreate(EventoAsistenteBase):
    evento_id: int
    usuario_id: int


class EventoAsistenteRead(EventoAsistenteBase):
    id: int
    creado_en: datetime

    class Config:
        from_attributes = True
