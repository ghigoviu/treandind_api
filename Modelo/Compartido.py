from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from Modelo import Base


class Compartido(Base):
    __tablename__ = 'compartidos'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=True)
    evento_id = Column(Integer, ForeignKey('eventos.id'), nullable=True)
    amigo_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  # Usuario al que se le comparte
    mensaje = Column(String(255), nullable=True)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    # Relaciones
    usuario = relationship("Usuario", backref="compartidos")
    amigo = relationship("Usuario", foreign_keys=[amigo_id], backref="compartidos_recibidos")
    producto = relationship("Producto", backref="compartidos")
    evento = relationship("Evento", backref="compartidos")

    def __init__(self, usuario_id, amigo_id, mensaje=None, producto_id=None, evento_id=None):
        self.usuario_id = usuario_id
        self.amigo_id = amigo_id
        self.mensaje = mensaje
        self.producto_id = producto_id
        self.evento_id = evento_id
