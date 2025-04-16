from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from Modelo import Base


class Amistad(Base):
    __tablename__ = 'amistades'

    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String(20), default='pendiente')  # pendiente, aceptada, rechazada
    creado_en = Column(DateTime, default=func.now(), nullable=False)
    amigo_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship("Usuario", foreign_keys=[usuario_id], back_populates="amistades_enviadas")
    amigo = relationship("Usuario", foreign_keys=[amigo_id], back_populates="amistades_recibidas")

    def __init__(self, usuario_id, amigo_id, estado, creado_en):
        self.estado = estado
        self.creado_en = creado_en
        self.usuario_id = usuario_id
        self.amigo_id = amigo_id
