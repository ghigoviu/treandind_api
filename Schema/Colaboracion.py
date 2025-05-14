from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HighlightBase(BaseModel):
    desc: str
    img: Optional[str] = None
    video: Optional[str] = None


class HighlightCreate(HighlightBase):
    usuario_id: int


class HighlightUpdate(BaseModel):
    desc: Optional[str] = None
    img: Optional[str] = None
    video: Optional[str] = None


class HighlightRead(HighlightBase):
    id: int
    usuario_id: int
    creado_en: datetime

    class Config:
        orm_mode = True
