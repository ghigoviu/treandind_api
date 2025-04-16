from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Modelo import Base


class ProductoImagen(Base):
    __tablename__ = 'producto_imagenes'

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    url = Column(String(255), nullable=False)
    es_portada = Column(Boolean, default=False)

    # Relación
    producto = relationship("Producto", backref="imagenes")

    def __init__(self, producto_id, url, es_portada=False):
        self.producto_id = producto_id
        self.url = url
        self.es_portada = es_portada
