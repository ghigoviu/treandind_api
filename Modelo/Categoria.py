from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from Modelo import Base


class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    imagen = Column(String(255), nullable=True)

    productos = relationship("Producto", back_populates="categoria")  # ← Relación inversa
