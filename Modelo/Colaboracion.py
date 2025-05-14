from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from Modelo import Base


class Colaboracion(Base):
    __tablename__ = 'colaboracion'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    usuarios = relationship("ColaboracionUsuario", back_populates="colaboracion")

    def __init__(self, nombre):
        self.nombre = nombre
