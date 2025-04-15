from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CompartidoBase(BaseModel):
    mensaje: Optional[str] = None


class CompartidoCreate(CompartidoBase):
    usuario_id: int
    amigo_id: int
    producto_id: Optional[int] = None
    evento_id: Optional[int] = None


class CompartidoRead(CompartidoBase):
    id: int
    creado_en: datetime

    class Config:
        orm_mode = True
