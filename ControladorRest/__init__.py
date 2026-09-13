from Datos.ManejadorBD import ManejadorBD

# Se reutiliza la única sesión definida por el ManejadorBD (Singleton), en vez
# de crear un segundo sessionmaker. Así hay una sola fuente de sesiones/engine.
handler = ManejadorBD()
SessionLocal = handler.getSesion()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
