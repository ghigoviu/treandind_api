from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from Modelo import Base


class Seguidor(Base):
    __tablename__ = 'seguidores'

    id = Column(Integer, primary_key=True, index=True)
    seguidor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    seguido_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    # Restricción: un usuario solo puede seguir a otro una vez.
    __table_args__ = (
        UniqueConstraint('seguidor_id', 'seguido_id', name='uq_seguidor_seguido'),
    )

    seguidor = relationship("Usuario", foreign_keys=[seguidor_id], backref="siguiendo")
    seguido = relationship("Usuario", foreign_keys=[seguido_id], backref="seguidores_rel")

    def __init__(self, seguidor_id, seguido_id):
        self.seguidor_id = seguidor_id
        self.seguido_id = seguido_id
