from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

from Schema.Base.Usuario import UsuarioRead
from Schema.Categoria import CategoriaRead
from Schema.ProductoAtributo import ProductoAtributoRead
from Schema.ProductoImagen import ProductoImagenRead
from Schema.Review import ReviewRead

TIPOS_PRODUCTO_VALIDOS = ('fisico', 'servicio', 'evento')


class AtributoAnidado(BaseModel):
    """Atributo para crear junto con el producto (sin producto_id, aún no existe)."""
    nombre: str
    valor: str


class ImagenAnidada(BaseModel):
    """Imagen para crear junto con el producto (sin producto_id, aún no existe)."""
    url: str
    es_portada: bool = False


class ProductoBase(BaseModel):
    nombre: str
    precio: float
    stock: int = 0
    tipo: str = 'fisico'
    categoria_id: Optional[int] = None
    requiere_edad: bool = False

    @field_validator('tipo')
    def validar_tipo(cls, v):
        if v and v not in TIPOS_PRODUCTO_VALIDOS:
            raise ValueError(f"tipo debe ser uno de: {', '.join(TIPOS_PRODUCTO_VALIDOS)}")
        return v or 'fisico'


class ProductoRead(ProductoBase):
    id: int
    calificacion: float
    oculto: bool = False
    vip: bool = False
    creado_en: datetime
    descripcion: Optional[str] = None
    img_portada: Optional[str] = None
    usuario_id: Optional[int] = None
    categoria: Optional[CategoriaRead] = None
    usuario_creador: Optional[UsuarioRead] = None

    class Config:
        from_attributes = True


class ProductoSchema(ProductoRead):
    atributos: List[ProductoAtributoRead] = []
    imagenes: List[ProductoImagenRead] = []
    reviews: List[ReviewRead] = []


class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int = 0
    tipo: str = 'fisico'
    descripcion: Optional[str] = None
    img_portada: Optional[str] = None
    usuario_id: int
    categoria_id: Optional[int] = None
    colaboracion_id: Optional[int] = None
    requiere_edad: bool = False
    vip: bool = False
    atributos: List[AtributoAnidado] = []
    imagenes: List[ImagenAnidada] = []

    @field_validator('tipo')
    def validar_tipo(cls, v):
        if v and v not in TIPOS_PRODUCTO_VALIDOS:
            raise ValueError(f"tipo debe ser uno de: {', '.join(TIPOS_PRODUCTO_VALIDOS)}")
        return v or 'fisico'


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    tipo: Optional[str] = None
    oculto: Optional[bool] = None
    vip: Optional[bool] = None
    categoria_id: Optional[int] = None
    requiere_edad: Optional[bool] = None
    img_portada: Optional[str] = None

    @field_validator('tipo')
    def validar_tipo(cls, v):
        if v and v not in TIPOS_PRODUCTO_VALIDOS:
            raise ValueError(f"tipo debe ser uno de: {', '.join(TIPOS_PRODUCTO_VALIDOS)}")
        return v
