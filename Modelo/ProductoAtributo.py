from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Modelo import Base


class ProductoAtributo(Base):
    __tablename__ = 'producto_atributos'

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    nombre = Column(String(50), nullable=False)
    valor = Column(String(100), nullable=False)

    # Relación
    producto = relationship("Producto", backref="atributos")

    def __init__(self, producto_id, nombre, valor):
        self.producto_id = producto_id
        self.nombre = nombre
        self.valor = valor
