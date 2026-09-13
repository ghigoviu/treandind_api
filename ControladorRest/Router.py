from fastapi import FastAPI

from Datos.Config import get_host_config
from ControladorRest.Usuario import UsuarioRest
from ControladorRest.Colaboracion import ColaboracionRest
from ControladorRest.Categoria import CategoriaRest
from ControladorRest.Amistad import AmistadRest
from ControladorRest.Evento import EventoRest
from ControladorRest.Producto import ProductoRest
from ControladorRest.Review import ReviewRest
from ControladorRest.Orden import OrdenRest
from ControladorRest.Compartido import CompartidoRest
from ControladorRest.Highlight import HighlightRest
from ControladorRest.Seguidor import SeguidorRest
from ControladorRest.PerfilVendedor import PerfilVendedorRest
from ControladorRest.Notificacion import NotificacionRest
from ControladorRest.Estadistica import EstadisticaRest
from ControladorRest.Membresia import MembresiaRest

app = FastAPI(title="API para aplicación de Treanding de Usuario")

# Incluimos el router de la clase UsuarioRest
app.include_router(ColaboracionRest.router)
app.include_router(UsuarioRest.router)
app.include_router(ProductoRest.router)
app.include_router(CategoriaRest.router)
app.include_router(AmistadRest.router)
app.include_router(EventoRest.router)
app.include_router(ReviewRest.router)
app.include_router(OrdenRest.router)
app.include_router(CompartidoRest.router)
app.include_router(HighlightRest.router)
app.include_router(SeguidorRest.router)
app.include_router(PerfilVendedorRest.router)
app.include_router(NotificacionRest.router)
app.include_router(EstadisticaRest.router)
app.include_router(MembresiaRest.router)

host_info = get_host_config()
