from pydantic import BaseModel
from typing import Optional, List


class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]


class CategoriaRead(CategoriaBase):
    id: int

    class Config:
        from_attributes = True
