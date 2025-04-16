from fastapi import FastAPI
import uvicorn

from ControladorRest.Usuario import UsuarioRest
from ControladorRest.Categoria import CategoriaRest
from ControladorRest.Amistad import AmistadRest
from ControladorRest.Evento import EventoRest
from ControladorRest.Producto import ProductoRest
from ControladorRest.Review import ReviewRest
from Datos.ManejadorBD import ManejadorBD

app = FastAPI(title="API para aplicación de Treanding de Usuario")

# Incluimos el router de la clase UsuarioRest
app.include_router(UsuarioRest.router)
app.include_router(ProductoRest.router)
app.include_router(CategoriaRest.router)
app.include_router(AmistadRest.router)
app.include_router(EventoRest.router)
app.include_router(ReviewRest.router)


if __name__ == '__main__':
    handler = ManejadorBD()
    handler.crear_bd()
    uvicorn.run(app, port=8081, host='localhost')
