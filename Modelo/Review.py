from sqlalchemy import Column, Integer, Text, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from Modelo import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=True)
    evento_id = Column(Integer, ForeignKey('eventos.id'), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    calificacion = Column(Float, nullable=False)
    comentario = Column(Text, nullable=True)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    # Relaciones
    producto = relationship("Producto", backref="reviews")
    evento = relationship("Evento", backref="reviews")
    usuario = relationship("Usuario", backref="reviews")

    def __init__(self, usuario_id, calificacion, comentario=None, producto_id=None, evento_id=None):
        self.usuario_id = usuario_id
        self.calificacion = calificacion
        self.comentario = comentario
        self.producto_id = producto_id
        self.evento_id = evento_id
