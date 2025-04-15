from pydantic import BaseModel


class ProductoAtributoBase(BaseModel):
    nombre: str
    valor: str


class ProductoAtributoCreate(ProductoAtributoBase):
    producto_id: int


class ProductoAtributoRead(ProductoAtributoBase):
    id: int

    class Config:
        orm_mode = True
