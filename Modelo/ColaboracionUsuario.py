from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from Modelo import Base


class ColaboracionUsuario(Base):
    __tablename__ = 'colaboracion_usuario'

    id = Column(Integer, primary_key=True, index=True)
    porcentaje = Column(Integer, nullable=False, default=0)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    colaboracion_id = Column(Integer, ForeignKey('colaboracion.id'), nullable=False)

    usuario = relationship("Usuario", back_populates="colaboraciones")
    colaboracion = relationship("Colaboracion", back_populates="usuarios")

    def __init__(self, usuario_id, colaboracion_id, porcentaje):
        self.porcentaje = porcentaje
        self.usuario_id = usuario_id
        self.colaboracion_id = colaboracion_id
