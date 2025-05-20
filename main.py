import uvicorn
from ControladorRest.Router import app, host_info

from Datos.ManejadorBD import ManejadorBD


if __name__ == '__main__':
    handler = ManejadorBD()
    handler.crear_bd()
    uvicorn.run(app, port=int(host_info['port']), host=host_info['add'])
