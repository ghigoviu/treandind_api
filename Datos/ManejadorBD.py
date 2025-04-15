from Datos.ConexionBD import ConexionBD


class SingletonMeta(type):

    _instances = {}

    def __call__(clase, *args, **kwargs):
        if clase not in clase._instances:
            instance = super().__call__(*args, **kwargs)
            clase._instances[clase] = instance
        return clase._instances[clase]


class ManejadorBD(metaclass=SingletonMeta):

    def __init__(self):
        self.conexion = ConexionBD()
        self.engine = self.conexion.get_engine()
        self.base = self.conexion.getBase()
        self.sesion = self.conexion.get_session()

    def getSesion(self):
        return self.sesion

    def getEngine(self):
        return self.engine

    def getBase(self):
        return self.base

    def crear_bd(self):
        self.base.metadata.create_all(self.getEngine())
        