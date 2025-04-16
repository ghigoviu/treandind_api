from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from Modelo import Base


class Orden(Base):
    __tablename__ = 'ordenes'

    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String(20), nullable=False)  # Ej: "pendiente", "completada", "cancelada"
    total = Column(Float, nullable=False)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    # Relación
    usuario = relationship("Usuario", backref="ordenes")
    detalles = relationship("OrdenDetalle", backref="orden", cascade="all, delete-orphan")

    def __init__(self, usuario_id, estado, total):
        self.usuario_id = usuario_id
        self.estado = estado
        self.total = total
