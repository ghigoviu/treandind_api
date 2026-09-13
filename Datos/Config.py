"""
Módulo central de configuración de la API.

Lee `config.ini` una sola vez y expone las secciones `mysql` y `host` para el
resto de la aplicación, evitando el doble parseo que existía en
`ControladorRest/Router.py` y `Datos/ConexionBD.py`.

El comportamiento es configurable por variables de entorno (útil para tests y
despliegues) con fallback a `config.ini` y, finalmente, a valores por defecto
sensatos para desarrollo local con XAMPP.
"""
import os
from configparser import ConfigParser
from functools import lru_cache


# Ruta del config.ini (por defecto en la raíz del proyecto, junto a main.py).
CONFIG_PATH = os.environ.get("TREANDING_CONFIG", "config.ini")


def _leer_ini() -> ConfigParser:
    parser = ConfigParser()
    # read() no falla si el archivo no existe: simplemente no carga secciones.
    parser.read(CONFIG_PATH)
    return parser


def _valor(ini: ConfigParser, seccion: str, clave: str, default=None):
    if ini.has_option(seccion, clave):
        return ini.get(seccion, clave)
    return default


@lru_cache(maxsize=1)
def get_mysql_config() -> dict:
    """Configuración de conexión MySQL.

    Precedencia: variables de entorno > config.ini [mysql] > defaults locales.
    """
    ini = _leer_ini()

    env_pass = os.environ.get("MYSQL_PASSWORD")
    return {
        "user": os.environ.get("MYSQL_USER") or _valor(ini, "mysql", "user", "root"),
        "passwd": env_pass if env_pass is not None else _valor(ini, "mysql", "passwd", ""),
        "host": os.environ.get("MYSQL_HOST") or _valor(ini, "mysql", "host", "localhost"),
        "port": int(os.environ.get("MYSQL_PORT") or _valor(ini, "mysql", "port", "3306")),
        "db": os.environ.get("MYSQL_DB") or _valor(ini, "mysql", "db", "treanding"),
    }


@lru_cache(maxsize=1)
def get_host_config() -> dict:
    """Configuración del host donde se sirve la API (uvicorn)."""
    ini = _leer_ini()
    return {
        "add": os.environ.get("API_HOST") or _valor(ini, "host", "add", "127.0.0.1"),
        "port": os.environ.get("API_PORT") or _valor(ini, "host", "port", "8081"),
    }


def get_database_url() -> str:
    """Construye la URL de conexión SQLAlchemy para MySQL."""
    cfg = get_mysql_config()
    passwd = cfg["passwd"] or ""
    auth = f"{cfg['user']}:{passwd}" if passwd else cfg["user"]
    return f"mysql://{auth}@{cfg['host']}:{cfg['port']}/{cfg['db']}"


def get_echo() -> bool:
    """Si el engine debe volcar el SQL a consola. Default: False."""
    valor = os.environ.get("SQL_ECHO")
    if valor is not None:
        return valor.strip().lower() in ("1", "true", "yes", "on")
    ini = _leer_ini()
    return _valor(ini, "mysql", "echo", "false").strip().lower() in ("1", "true", "yes", "on")


@lru_cache(maxsize=1)
def get_email_config() -> dict:
    """Configuración SMTP para el envío de correos.

    Precedencia: variables de entorno > config.ini [email] > defaults.
    `enabled` desactiva el envío real (útil en dev/tests); `admin` es el correo
    del administrador del sitio.
    """
    ini = _leer_ini()

    enabled_env = os.environ.get("EMAIL_ENABLED")
    if enabled_env is not None:
        enabled = enabled_env.strip().lower() in ("1", "true", "yes", "on")
    else:
        enabled = _valor(ini, "email", "enabled", "false").strip().lower() in ("1", "true", "yes", "on")

    return {
        "enabled": enabled,
        "host": os.environ.get("SMTP_HOST") or _valor(ini, "email", "host", "localhost"),
        "port": int(os.environ.get("SMTP_PORT") or _valor(ini, "email", "port", "1025")),
        "user": os.environ.get("SMTP_USER") or _valor(ini, "email", "user", ""),
        "password": os.environ.get("SMTP_PASSWORD")
        if os.environ.get("SMTP_PASSWORD") is not None
        else _valor(ini, "email", "password", ""),
        "from": os.environ.get("EMAIL_FROM") or _valor(ini, "email", "from", "no-reply@treanding.local"),
        "admin": os.environ.get("EMAIL_ADMIN") or _valor(ini, "email", "admin", "admin@treanding.local"),
    }


def reset_cache() -> None:
    """Limpia la cache de configuración (útil en tests al cambiar el entorno)."""
    get_mysql_config.cache_clear()
    get_host_config.cache_clear()
    get_email_config.cache_clear()
