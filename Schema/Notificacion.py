from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificacionRead(BaseModel):
    id: int
    usuario_id: int
    tipo: str
    mensaje: str
    ref_id: Optional[int] = None
    leida: bool
    creado_en: datetime

    class Config:
        from_attributes = True
