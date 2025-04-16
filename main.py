from fastapi import FastAPI
import uvicorn

from ControladorRest.Usuario import UsuarioRest
from ControladorRest.Categoria import CategoriaRest
from ControladorRest.Amistad import AmistadRest
from Datos.ManejadorBD import ManejadorBD

app = FastAPI(title="API para aplicación de Treanding de Usuario")

# Incluimos el router de la clase UsuarioRest
app.include_router(UsuarioRest.router)
app.include_router(CategoriaRest.router)
app.include_router(AmistadRest.router)


if __name__ == '__main__':
    handler = ManejadorBD()
    handler.crear_bd()
    uvicorn.run(app, port=8081, host='localhost')
