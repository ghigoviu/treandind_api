from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewBase(BaseModel):
    calificacion: float
    comentario: Optional[str] = None


class ReviewCreate(ReviewBase):
    usuario_id: int
    producto_id: Optional[int] = None
    evento_id: Optional[int] = None


class ReviewRead(ReviewBase):
    id: int
    producto_id: Optional[int] = None
    evento_id: Optional[int] = None
    usuario_id: int
    creado_en: datetime

    class Config:
        from_attributes = True


class ReviewUpdate(BaseModel):
    usuario_id: int
    calificacion: Optional[float]
    comentario: Optional[str] = None
    producto_id: Optional[int] = None
    evento_id: Optional[int] = None
