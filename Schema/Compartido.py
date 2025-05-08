from typing import Optional
from Schema.Base.Usuario import UsuarioRead
from Schema.Producto import ProductoRead
from Schema.Evento import EventoRead
from Schema.Base.Compartido import CompartidoRead


class CompartidoSchema(CompartidoRead):
    amigo: Optional[UsuarioRead] = None
    producto: Optional[ProductoRead] = None
    evento: Optional[EventoRead] = None

