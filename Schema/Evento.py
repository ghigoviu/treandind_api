from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class EventoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None
    categoria: str = "Evento"
    fecha: datetime
    ubicacion: str
    img_evento: Optional[str] = None
    img_flyer: Optional[str] = None
    boletos_total: int = 0
    calificacion: Optional[float] = 0.0


class EventoCreate(EventoBase):
    usuario_id: int


class EventoRead(EventoBase):
    id: int
    boletos_disponibles: int = 0
    creado_en: datetime

    class Config:
        from_attributes = True


class EventoAsistenteRead(BaseModel):
    id: int
    usuario_id: int
    estado: str
    creado_en: datetime

    class Config:
        from_attributes = True


class EventoConAsistentes(EventoRead):
    asistentes: List[EventoAsistenteRead]
    total_asistentes: int


class EventoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    fecha: Optional[datetime] = None
    ubicacion: Optional[str] = None
    img_evento: Optional[str] = None
    img_flyer: Optional[str] = None
    boletos_total: Optional[int] = None

    class Config:
        from_attributes = True