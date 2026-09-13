from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from Modelo import Base


class Notificacion(Base):
    __tablename__ = 'notificaciones'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  # destinatario
    tipo = Column(String(30), nullable=False)  # amistad, venta, seguidor, invitacion, nuevo_producto
    mensaje = Column(String(255), nullable=False)
    ref_id = Column(Integer, nullable=True)  # id relacionado (producto, amistad, etc.)
    leida = Column(Boolean, nullable=False, default=False)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    usuario = relationship("Usuario", backref="notificaciones")

    def __init__(self, usuario_id, tipo, mensaje, ref_id=None):
        self.usuario_id = usuario_id
        self.tipo = tipo
        self.mensaje = mensaje
        self.ref_id = ref_id
