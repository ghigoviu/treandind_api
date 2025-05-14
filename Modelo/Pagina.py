from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from Modelo import Base


class Pagina(Base):
    __tablename__ = 'pagina'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    contenido = Column(Text, nullable=True)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    colaboracion_id = Column(Integer, ForeignKey('colaboracion.id'), nullable=False)

    # Relaciones
    autor = relationship("Usuario", back_populates="paginas")
    colab = relationship("Colaboracion", back_populates="paginas")

    def __init__(self, titulo, contenido, usuario_id = None, colaboracion_id = None):
        self.tiulo = titulo
        self.contenido = contenido
        self.usuario_id = usuario_id
        self.colaboracion_id = colaboracion_id
