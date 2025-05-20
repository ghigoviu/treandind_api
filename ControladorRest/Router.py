from fastapi import FastAPI
from configparser import ConfigParser

from ControladorRest.Usuario import UsuarioRest
from ControladorRest.Categoria import CategoriaRest
from ControladorRest.Amistad import AmistadRest
from ControladorRest.Evento import EventoRest
from ControladorRest.Producto import ProductoRest
from ControladorRest.Review import ReviewRest
from ControladorRest.Orden import OrdenRest
from ControladorRest.Compartido import CompartidoRest
from ControladorRest.Highlight import HighlightRest

app = FastAPI(title="API para aplicación de Treanding de Usuario")

# Incluimos el router de la clase UsuarioRest
app.include_router(UsuarioRest.router)
app.include_router(ProductoRest.router)
app.include_router(CategoriaRest.router)
app.include_router(AmistadRest.router)
app.include_router(EventoRest.router)
app.include_router(ReviewRest.router)
app.include_router(OrdenRest.router)
app.include_router(CompartidoRest.router)
app.include_router(HighlightRest.router)

config_object = ConfigParser()
config_object.read('config.ini')
host_info = config_object['host']
