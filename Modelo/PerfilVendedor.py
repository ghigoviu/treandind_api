from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from Modelo import Base


class PerfilVendedor(Base):
    __tablename__ = 'perfil_vendedor'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), unique=True, nullable=False)
    metodos_entrega = Column(Text, nullable=True)
    lugares_entrega = Column(Text, nullable=True)
    info_general = Column(Text, nullable=True)
    datos_bancarios = Column(Text, nullable=True)
    validado = Column(Boolean, nullable=False, default=False)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    usuario = relationship("Usuario", backref="perfil_vendedor")

    def __init__(self, usuario_id, metodos_entrega=None, lugares_entrega=None,
                 info_general=None, datos_bancarios=None, **kwargs):
        self.usuario_id = usuario_id
        self.metodos_entrega = metodos_entrega
        self.lugares_entrega = lugares_entrega
        self.info_general = info_general
        self.datos_bancarios = datos_bancarios
