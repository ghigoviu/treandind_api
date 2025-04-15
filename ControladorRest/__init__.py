from sqlalchemy.orm import sessionmaker

from Datos.ManejadorBD import ManejadorBD

handler = ManejadorBD()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=handler.getEngine())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()