from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from Schema.Base.Usuario import UsuarioRead
from Schema.Categoria import CategoriaRead
from Schema.ProductoAtributo import ProductoAtributoRead
from Schema.ProductoImagen import ProductoImagenRead
from Schema.Review import ReviewRead


class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int
    categoria_id: Optional[int] = None
    requiere_edad: bool = False


class ProductoRead(ProductoBase):
    id: int
    calificacion: float
    creado_en: datetime
    descripcion: Optional[str] = None
    img_portada: Optional[str] = None
    categoria: Optional[CategoriaRead] = []
    usuario_creador: Optional[UsuarioRead] = None

    class Config:
        from_attributes = True


class ProductoSchema(ProductoRead):
    atributos: List[ProductoAtributoRead] = []
    imagenes: List[ProductoImagenRead] = []
    reviews: List[ReviewRead] = []


class ProductoCreate(ProductoBase):
    usuario_id: int


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    categoria_id: Optional[int] = None
    requiere_edad: Optional[bool] = None
