from typing import List

from Schema.Amistad import AmistadUsuario, AmistadAmigo
from Schema.Compartido import CompartidoSchema
from Schema.Base.Usuario import UsuarioRead
from Schema.Producto import ProductoRead


class UsuarioSchema(UsuarioRead):
    amistades_enviadas: List[AmistadAmigo] = []
    amistades_recibidas: List[AmistadUsuario] = []
    compartidos: List[CompartidoSchema] = []
    productos: List[ProductoRead] = []
