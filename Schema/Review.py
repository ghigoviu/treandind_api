from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

from Schema.Base.Usuario import UsuarioRead


def _validar_rango(v):
    """Valida que la calificación esté en el rango 1-5 (inclusive)."""
    if v is None:
        return v
    if v < 1 or v > 5:
        raise ValueError("La calificación debe estar entre 1 y 5.")
    return v


class ReviewBase(BaseModel):
    calificacion: float
    comentario: Optional[str] = None

    @field_validator("calificacion")
    def calificacion_en_rango(cls, v):
        return _validar_rango(v)


class ReviewCreate(ReviewBase):
    usuario_id: int
    producto_id: Optional[int] = None
    evento_id: Optional[int] = None


class ReviewRead(ReviewBase):
    id: int
    usuario: Optional[UsuarioRead] = None
    producto_id: Optional[int] = None
    evento_id: Optional[int] = None
    creado_en: datetime

    class Config:
        from_attributes = True


class ReviewUpdate(BaseModel):
    usuario_id: int
    calificacion: Optional[float] = None
    comentario: Optional[str] = None
    producto_id: Optional[int] = None
    evento_id: Optional[int] = None

    @field_validator("calificacion")
    def calificacion_en_rango(cls, v):
        return _validar_rango(v)
