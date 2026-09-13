from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from Datos.Config import get_database_url, get_echo


class ConexionBD:
    def __init__(self):
        url = get_database_url()
        # pool_pre_ping evita errores "MySQL server has gone away" en conexiones
        # ociosas. echo es configurable (default False) para no volcar SQL a logs.
        self.mysql_engine = create_engine(url, echo=get_echo(), pool_pre_ping=True)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.mysql_engine)
        self.Base = declarative_base()

    def get_engine(self):
        return self.mysql_engine

    def get_session(self):
        return self.session

    def getBase(self):
        return self.Base
