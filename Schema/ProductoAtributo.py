from pydantic import BaseModel


class ProductoAtributoBase(BaseModel):
    nombre: str
    valor: str


class ProductoAtributoRead(ProductoAtributoBase):
    id: int

    class Config:
        from_attributes = True


class ProductoAtributoCreate(ProductoAtributoBase):
    producto_id: int
