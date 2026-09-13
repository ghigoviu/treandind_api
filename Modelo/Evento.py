from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from Modelo import Base


class Evento(Base):
    __tablename__ = 'eventos'

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nombre = Column(String(100), nullable=False)
    precio = Column(Float, nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(50), nullable=False)  # Ej: "Evento", "Charity", etc.
    fecha = Column(DateTime, nullable=False)
    ubicacion = Column(String(255), nullable=False)
    img_evento = Column(String(255), nullable=True)
    img_flyer = Column(String(255), nullable=True)
    boletos_total = Column(Integer, nullable=False, default=0)
    boletos_disponibles = Column(Integer, nullable=False, default=0)
    calificacion = Column(Float, default=0.0)
    creado_en = Column(DateTime, default=func.now(), nullable=False)

    # Relación
    usuario_creador = relationship("Usuario", back_populates="eventos")

    def __init__(self, usuario_id, nombre, precio, descripcion, categoria, fecha,
                 ubicacion, img_evento=None, img_flyer=None, boletos_total=0,
                 boletos_disponibles=None, calificacion=0.0, **kwargs):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.categoria = categoria
        self.fecha = fecha
        self.ubicacion = ubicacion
        self.img_evento = img_evento
        self.img_flyer = img_flyer
        self.boletos_total = boletos_total
        # Al crear, los disponibles arrancan igual al total salvo que se indique.
        self.boletos_disponibles = boletos_disponibles if boletos_disponibles is not None else boletos_total
        self.calificacion = calificacion
