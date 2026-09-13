from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from Modelo import Base


class SuscripcionMembresia(Base):
    """Suscripción de un visitante a un paquete de membresía de un vendedor."""
    __tablename__ = 'suscripciones_membresia'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  # suscriptor
    paquete_id = Column(Integer, ForeignKey('paquetes.id'), nullable=False)
    vendedor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    estado = Column(String(20), nullable=False, default='activa')  # activa, vencida, cancelada
    inicio = Column(DateTime, default=func.now(), nullable=False)
    vencimiento = Column(DateTime, nullable=False)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    usuario = relationship("Usuario", foreign_keys=[usuario_id], backref="suscripciones")
    paquete = relationship("Paquete", backref="suscripciones")

    def __init__(self, usuario_id, paquete_id, vendedor_id, vencimiento, estado='activa', **kwargs):
        self.usuario_id = usuario_id
        self.paquete_id = paquete_id
        self.vendedor_id = vendedor_id
        self.vencimiento = vencimiento
        self.estado = estado
