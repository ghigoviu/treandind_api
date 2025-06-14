from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ColaboracionBase(BaseModel):
    desc: str
    img: Optional[str] = None
    video: Optional[str] = None


class ColaboracionCreate(ColaboracionBase):
    usuario_id: int


class ColaboracionUpdate(BaseModel):
    desc: Optional[str] = None
    img: Optional[str] = None
    video: Optional[str] = None


class ColaboracionRead(ColaboracionBase):
    id: int
    usuario_id: int
    creado_en: datetime

    class Config:
        from_attributes = True
