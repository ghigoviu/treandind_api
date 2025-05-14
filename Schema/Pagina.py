from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaginaBase(BaseModel):
    desc: Optional[str] = None
    img: Optional[str] = None
    vdeo: Optional[str] = None


class HighlightCreate(PaginaBase):
    usuario_id: int
    desc: Optional[str] = None
    img: Optional[str] = None
    vdeo: Optional[str] = None


class HighlightRead(PaginaBase):
    id: int
    usuario_id: int
    creado_en: datetime

    class Config:
        from_attributes = True
