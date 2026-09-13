from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ColaboracionBase(BaseModel):
    desc: str
    nombre_comercial: Optional[str] = None
    img: Optional[str] = None
    video: Optional[str] = None


class ColaboracionCreate(ColaboracionBase):
    usuario_id: int


class ColaboracionUpdate(BaseModel):
    desc: Optional[str] = None
    nombre_comercial: Optional[str] = None
    img: Optional[str] = None
    video: Optional[str] = None


class ColaboracionRead(ColaboracionBase):
    id: int
    usuario_id: int
    creado_en: datetime

    class Config:
        from_attributes = True


class InvitarMiembro(BaseModel):
    usuario_id: int
    porcentaje_sugerido: int = 0


class ResponderInvitacion(BaseModel):
    """El invitado acepta el % sugerido o replica proponiendo su propio %."""
    accion: str  # 'aceptar' | 'replicar'
    porcentaje: Optional[int] = None  # requerido si accion == 'replicar'
