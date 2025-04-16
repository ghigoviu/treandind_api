from configparser import ConfigParser
import io

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class ConexionBD:
    def __init__(self):
        configfile_name = "config.ini"
        config_object = ConfigParser()
        config_object.read('config.ini')
        mysql_info = config_object['mysql']
        # Load the configuration file

        user = mysql_info['user']
        passw = mysql_info['passwd']
        host = mysql_info['host']
        port = 3306
        db = mysql_info['db']
        url = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(user, passw, host, port, db)
        print(url)
        self.mysql_engine = create_engine(url, echo=False)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.mysql_engine)
        self.Base = declarative_base()

    def get_engine(self):
        return self.mysql_engine

    def get_session(self):
        return self.session

    def getBase(self):
        return self.Base
