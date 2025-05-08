from typing import List

from Schema.Amistad import AmistadRead
from Schema.Compartido import CompartidoSchema
from Schema.Base.Usuario import UsuarioRead


class UsuarioSchema(UsuarioRead):
    amistades_enviadas: List[AmistadRead] = []
    amistades_recibidas: List[AmistadRead] = []
    compartidos: List[CompartidoSchema] = []
