from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

FRECUENCIAS_VALIDAS = ('mensual', 'semestral', 'anual')


class PaqueteCreate(BaseModel):
    vendedor_id: int
    titulo: str
    frecuencia: str
    costo: float
    descripcion: Optional[str] = None
    imagen: Optional[str] = None

    @field_validator('frecuencia')
    def validar_frecuencia(cls, v):
        if v not in FRECUENCIAS_VALIDAS:
            raise ValueError(f"frecuencia debe ser una de: {', '.join(FRECUENCIAS_VALIDAS)}")
        return v


class PaqueteRead(BaseModel):
    id: int
    vendedor_id: int
    titulo: str
    frecuencia: str
    costo: float
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    creado_en: datetime

    class Config:
        from_attributes = True


class SuscribirRequest(BaseModel):
    usuario_id: int
    paquete_id: int


class SuscripcionRead(BaseModel):
    id: int
    usuario_id: int
    paquete_id: int
    vendedor_id: int
    estado: str
    inicio: datetime
    vencimiento: datetime

    class Config:
        from_attributes = True
