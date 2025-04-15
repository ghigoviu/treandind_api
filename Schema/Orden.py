from pydantic import BaseModel
from datetime import datetime


class OrdenBase(BaseModel):
    estado: str  # Ej: "pendiente", "completada", "cancelada"
    total: float


class OrdenCreate(OrdenBase):
    usuario_id: int


class OrdenRead(OrdenBase):
    id: int
    creado_en: datetime

    class Config:
        orm_mode = True
