from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from Modelo import Base


class Evento(Base):
    __tablename__ = 'eventos'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(50), nullable=False)  # Ej: "Evento", "Charity", etc.
    fecha = Column(DateTime, nullable=False)
    ubicacion = Column(String(255), nullable=False)
    img_evento = Column(String(255), nullable=True)
    calificacion = Column(Float, default=0.0)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    # Relación
    usuario = relationship("Usuario", back_populates="eventos")

    def __init__(self, usuario_id, nombre, precio, descripcion, categoria, fecha, ubicacion, img_evento=None, calificacion=0.0):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.categoria = categoria
        self.fecha = fecha
        self.ubicacion = ubicacion
        self.img_evento = img_evento
        self.calificacion = calificacion
