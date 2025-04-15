from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class ConexionBD:
    def __init__(self):
        user = 'plexodemos'
        passw = 'ksmhs.65Df.p9'
        host = 'localhost'
        port = 3306
        db = 'plexoweb_treanding'
        url = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(user, passw, host, port, db)
        self.mysql_engine = create_engine(url, echo=False)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.mysql_engine)
        self.Base = declarative_base()

    def get_engine(self):
        return self.mysql_engine

    def get_session(self):
        return self.session

    def getBase(self):
        return self.Base
