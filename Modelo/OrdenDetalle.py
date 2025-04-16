from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from Modelo import Base


class OrdenDetalle(Base):
    __tablename__ = 'orden_detalles'

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer, nullable=False)
    precio_unit = Column(Float, nullable=False)

    orden_id = Column(Integer, ForeignKey('ordenes.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=True)
    evento_id = Column(Integer, ForeignKey('eventos.id'), nullable=True)

    # Relaciones
    orden = relationship("Orden", backref="detalles")
    producto = relationship("Producto", backref="orden_detalles")
    evento = relationship("Evento", backref="orden_detalles")

    def __init__(self, orden_id, cantidad, precio_unit, producto_id=None, evento_id=None):
        self.orden_id = orden_id
        self.cantidad = cantidad
        self.precio_unit = precio_unit
        self.producto_id = producto_id
        self.evento_id = evento_id
