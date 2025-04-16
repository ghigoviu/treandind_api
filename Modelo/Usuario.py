from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from Modelo import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)  # Idealmente hash
    imagen_perfil = Column(String(255), nullable=True)  # URL puede ser larga
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    amistades_enviadas = relationship("Amistad", foreign_keys='Amistad.usuario_id', back_populates="usuario")
    amistades_recibidas = relationship("Amistad", foreign_keys='Amistad.amigo_id', back_populates="amigo")

    def __init__(self, nombre, email, password, imagen_perfil=None):
        self.nombre = nombre
        self.email = email
        self.password = password
        self.imagen_perfil = imagen_perfil
