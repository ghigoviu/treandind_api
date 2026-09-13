from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from Schema.Base.Usuario import UsuarioRead


class SeguidorCreate(BaseModel):
    seguidor_id: int
    seguido_id: int


class SeguidorRead(BaseModel):
    id: int
    seguidor_id: int
    seguido_id: int
    creado_en: datetime

    class Config:
        from_attributes = True


class SeguidorDetalle(BaseModel):
    """Seguidor/seguido con datos del usuario, para el frontend."""
    id: int
    nombre: str
    imagen_perfil: Optional[str] = None
    tipo_perfil: Optional[str] = None
