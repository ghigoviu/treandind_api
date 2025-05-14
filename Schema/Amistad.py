from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from Schema.Base.Usuario import UsuarioRead


class AmistadBase(BaseModel):
    usuario_id: int
    amigo_id: int
    estado: Optional[str] = "pendiente"

    @field_validator('estado')
    def validar_estado(cls, v):
        estados_validos = ["pendiente", "aceptada", "rechazada"]
        if v not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")
        return v


class AmistadCreate(AmistadBase):
    pass


class AmistadUpdate(BaseModel):
    estado: Optional[str]


class AmistadRead(BaseModel):
    id: int
    usuario_id: int
    amigo_id: int
    estado: Optional[str] = "pendiente"
    creado_en: datetime

    class Config:
        from_attributes = True


class AmistadUsuario(BaseModel):
    usuario: Optional[UsuarioRead] = None
    estado: Optional[str] = "pendiente"
    creado_en: datetime


class AmistadAmigo(BaseModel):
    amigo: Optional[UsuarioRead] = None
    estado: Optional[str] = "pendiente"
    creado_en: datetime