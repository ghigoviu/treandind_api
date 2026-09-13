from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from Modelo import Base


class Paquete(Base):
    """Paquete de membresía que un vendedor ofrece a sus visitantes VIP."""
    __tablename__ = 'paquetes'

    id = Column(Integer, primary_key=True, index=True)
    vendedor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    titulo = Column(String(100), nullable=False)
    frecuencia = Column(String(20), nullable=False)  # mensual, semestral, anual
    costo = Column(Float, nullable=False)
    descripcion = Column(Text, nullable=True)
    imagen = Column(String(255), nullable=True)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    vendedor = relationship("Usuario", backref="paquetes")

    def __init__(self, vendedor_id, titulo, frecuencia, costo, descripcion=None, imagen=None, **kwargs):
        self.vendedor_id = vendedor_id
        self.titulo = titulo
        self.frecuencia = frecuencia
        self.costo = costo
        self.descripcion = descripcion
        self.imagen = imagen
