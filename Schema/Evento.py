from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


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
    categoría: Optional[str] = None
    fecha: Optional[datetime] = None
    ubicacion: Optional[str] = None
    img_evento: Optional[str] = None

    class Config:
        from_attributes = True