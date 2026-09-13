from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

TIPOS_PERFIL_VALIDOS = ('visitante', 'vendedor', 'influencer')


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    tipo_perfil: Optional[str] = 'visitante'
    imagen_perfil: Optional[str] = None
    imagen_portada: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    verified: Optional[bool] = None
    birthdate: Optional[datetime] = None

    @field_validator('tipo_perfil')
    def validar_tipo_perfil(cls, v):
        if v and v not in TIPOS_PERFIL_VALIDOS:
            raise ValueError(f"tipo_perfil debe ser uno de: {', '.join(TIPOS_PERFIL_VALIDOS)}")
        return v or 'visitante'


class LoginRequest(BaseModel):
    email: str
    password: str


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioRead(UsuarioBase):
    id: int
    creado_en: datetime

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    tipo_perfil: Optional[str] = None
    imagen_perfil: Optional[str] = None
    imagen_portada: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[datetime] = None

    @field_validator('tipo_perfil')
    def validar_tipo_perfil(cls, v):
        if v and v not in TIPOS_PERFIL_VALIDOS:
            raise ValueError(f"tipo_perfil debe ser uno de: {', '.join(TIPOS_PERFIL_VALIDOS)}")
        return v

    class Config:
        from_attributes = True
