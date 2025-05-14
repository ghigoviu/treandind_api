from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from Modelo import Base


class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False, default='slug')
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    img_portada = Column(String(255), nullable=False, default="")
    creado_en = Column(DateTime, default=func.now(), nullable=False)
    requiere_edad = Column(Boolean, default=False)
    calificacion = Column(Float, default=0.0)  # precalculado

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    colaboracion_id = Column(Integer, ForeignKey('colaboracion.id'), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="productos")

    # Relaciones
    usuario_creador = relationship("Usuario", back_populates="productos")
    imagenes = relationship("ProductoImagen", back_populates="producto")
    atributos = relationship("ProductoAtributo", back_populates="producto")

    def __init__(self, nombre, descripcion, precio, stock, usuario_id, categoria_id=None,
                 requiere_edad=False, calificacion=0.0):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.usuario_id = usuario_id
        self.categoria_id = categoria_id
        self.requiere_edad = requiere_edad
        self.calificacion = calificacion
