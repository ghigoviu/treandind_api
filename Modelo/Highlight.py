from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import relationship
from Modelo import Base


class Highlight(Base):
    __tablename__ = 'highlights'

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)
    img = Column(String(255), nullable=False, default="")
    video = Column(String(255), nullable=False, default="")
    creado_en = Column(DateTime, default=func.now(), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    # Relación
    usuario = relationship("Usuario", backref="highlights")

    def __init__(self, usuario_id, estado, total):
        self.usuario_id = usuario_id
        self.estado = estado
        self.total = total
