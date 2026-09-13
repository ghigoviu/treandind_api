from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from sqlalchemy.orm import relationship

from Modelo import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)  # Idealmente hash
    tipo_perfil = Column(String(20), nullable=False, default='visitante')  # visitante, vendedor, influencer
    imagen_perfil = Column(String(255), nullable=True)
    imagen_portada = Column(String(255), nullable=True)
    bio = Column(String(100), nullable=False, default="New on Treanding")
    phone = Column(String(255), nullable=True)
    verified = Column(Boolean, nullable=True)
    birthdate = Column(DateTime, nullable=True, default=None)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    amistades_enviadas = relationship("Amistad", foreign_keys='Amistad.usuario_id', back_populates="usuario")
    amistades_recibidas = relationship("Amistad", foreign_keys='Amistad.amigo_id', back_populates="amigo")
    compartidos = relationship("Compartido", foreign_keys='Compartido.usuario_id')
    eventos = relationship("Evento", back_populates="usuario_creador")
    productos = relationship("Producto", back_populates="usuario_creador")
    colaboraciones = relationship("ColaboracionUsuario", back_populates="usuario")

    def __init__(self, nombre, email, password, tipo_perfil='visitante',
                 imagen_perfil=None, imagen_portada=None, bio=None,
                 phone=None, verified=None, birthdate=None, **kwargs):
        self.nombre = nombre
        self.email = email
        self.password = password
        self.tipo_perfil = tipo_perfil
        self.imagen_perfil = imagen_perfil
        self.imagen_portada = imagen_portada
        if bio is not None:
            self.bio = bio
        self.phone = phone
        self.verified = verified
        self.birthdate = birthdate

    def __str__(self):
        return f"Usuario (id={self.id!r}, nombre={self.nombre!r}, tipo={self.tipo_perfil!r})"
