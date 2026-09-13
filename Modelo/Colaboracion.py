from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from Modelo import Base


class Colaboracion(Base):
    __tablename__ = 'colaboracion'

    id = Column(Integer, primary_key=True, index=True)
    nombre_comercial = Column(String(100), nullable=True)
    desc = Column(Text, nullable=False)
    img = Column(String(255), nullable=True)
    video = Column(String(255), nullable=True)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    # Usuario creador de la colaboración.
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    # Miembros de la colaboración (tabla intermedia ColaboracionUsuario).
    usuarios = relationship("ColaboracionUsuario", back_populates="colaboracion")

    def __init__(self, desc, usuario_id, nombre_comercial=None, img=None, video=None, **kwargs):
        self.desc = desc
        self.usuario_id = usuario_id
        self.nombre_comercial = nombre_comercial
        self.img = img
        self.video = video
