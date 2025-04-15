from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from Modelo import Base


class EventoAsistente(Base):
    __tablename__ = 'evento_asistentes'

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey('eventos.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    estado = Column(String(20), nullable=False, default='pendiente')  # confirmada, pendiente, cancelada
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    # Relaciones
    evento = relationship("Evento", backref="asistentes")
    usuario = relationship("Usuario", backref="eventos_asistidos")

    def __init__(self, evento_id, usuario_id, estado='pendiente'):
        self.evento_id = evento_id
        self.usuario_id = usuario_id
        self.estado = estado
