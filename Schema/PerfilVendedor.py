from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PerfilVendedorCreate(BaseModel):
    usuario_id: int
    metodos_entrega: Optional[str] = None
    lugares_entrega: Optional[str] = None
    info_general: Optional[str] = None
    datos_bancarios: Optional[str] = None


class PerfilVendedorUpdate(BaseModel):
    metodos_entrega: Optional[str] = None
    lugares_entrega: Optional[str] = None
    info_general: Optional[str] = None
    datos_bancarios: Optional[str] = None


class PerfilVendedorRead(BaseModel):
    id: int
    usuario_id: int
    metodos_entrega: Optional[str] = None
    lugares_entrega: Optional[str] = None
    info_general: Optional[str] = None
    datos_bancarios: Optional[str] = None
    validado: bool
    creado_en: datetime

    class Config:
        from_attributes = True
