from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    imagen_perfil: Optional[str] = None


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
    imagen_perfil: Optional[str] = None

    class Config:
        from_attributes = True
