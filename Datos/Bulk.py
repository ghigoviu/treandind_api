"""
Migración / carga de datos semilla para Treanding.

Lee los archivos JSON de `Datos/data/` y los inserta en la base de datos usando
inserciones directas por columnas del modelo (evita los `__init__` custom de los
modelos, que son inconsistentes). El proceso es idempotente: vacía las tablas
afectadas y las recarga en orden de dependencias (respetando las FKs).

Uso:
    python -m Datos.Bulk           # carga contra la BD configurada (config.ini / env)

No modifica configuración del servidor MySQL; solo inserta filas.
"""
import json
import os
from datetime import datetime

from sqlalchemy import text

from Datos.ManejadorBD import ManejadorBD

# Importar todos los modelos que vamos a poblar (registra los mappers).
from Modelo.Usuario import Usuario
from Modelo.Categoria import Categoria
from Modelo.Producto import Producto
from Modelo.ProductoImagen import ProductoImagen
from Modelo.ProductoAtributo import ProductoAtributo
from Modelo.Amistad import Amistad
from Modelo.Evento import Evento
from Modelo.EventoAsistente import EventoAsistente
from Modelo.Review import Review
from Modelo.Compartido import Compartido
from Modelo.Highlight import Highlight


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def _leer_json(nombre_archivo: str) -> dict:
    """Lee un JSON de Datos/data tolerando encoding no-UTF8 (los seeds tienen
    caracteres en cp1252). Intenta utf-8 y cae a cp1252/latin-1."""
    ruta = os.path.join(DATA_DIR, nombre_archivo)
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            with open(ruta, "r", encoding=encoding) as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    # Último intento: utf-8 ignorando errores.
    with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
        return json.load(f)


def _parse_fecha(valor):
    """Convierte strings ISO (con o sin Z) a datetime; devuelve None si no aplica."""
    if not valor:
        return None
    if isinstance(valor, datetime):
        return valor
    texto = str(valor).replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(texto)
        # MySQL DATETIME no guarda tzinfo; lo quitamos.
        return dt.replace(tzinfo=None)
    except ValueError:
        return None


def _default_columna(columna):
    """Obtiene el valor por defecto de una columna, o None si es nullable."""
    default = columna.default
    if default is not None and getattr(default, "is_scalar", False):
        return default.arg
    return None


def _filtrar_columnas(modelo, fila: dict, mapeo=None, fechas=None) -> dict:
    """Normaliza una fila JSON a un dict con TODAS las columnas del modelo.

    En un bulk insert con lista de dicts, todas las filas deben compartir el
    mismo conjunto de claves; por eso rellenamos las columnas ausentes con su
    valor por defecto (o None si son nullable). Solo se descartan las columnas
    autoincrement/PK cuando no vienen en el JSON.

    - `mapeo`: dict {clave_json: columna_modelo} para renombrar campos.
    - `fechas`: iterable de columnas que deben parsearse como datetime.
    """
    mapeo = mapeo or {}
    fechas = set(fechas or [])
    columnas = {c.name: c for c in modelo.__table__.columns}

    # Primero, tomar los valores presentes en el JSON (renombrando y parseando).
    provistos = {}
    for clave, valor in fila.items():
        columna = mapeo.get(clave, clave)
        if columna not in columnas:
            continue
        if columna in fechas:
            valor = _parse_fecha(valor)
        provistos[columna] = valor

    # Luego, completar las columnas ausentes con su default (excepto la PK
    # autoincrement, que se resuelve aparte según descartar_id).
    resultado = {}
    for nombre, columna in columnas.items():
        if nombre in provistos:
            resultado[nombre] = provistos[nombre]
        elif columna.primary_key:
            # No forzar la PK; se decide fuera (id del JSON o autoincrement).
            continue
        else:
            resultado[nombre] = _default_columna(columna)

    # Conservar el id del JSON si venía (para modo no-autoincrement).
    if "id" in provistos:
        resultado["id"] = provistos["id"]
    return resultado


# Orden de carga: respeta las dependencias de claves foráneas.
# (tabla_sql, modelo, archivo_json, clave_en_json, mapeo, columnas_fecha, descartar_id)
# descartar_id=True: se ignora el "id" del JSON y se deja autoincrement (útil
# cuando el JSON tiene ids duplicados/poco fiables, como ProductoImagen).
PLAN = [
    ("usuarios", Usuario, "Usuario.json", "Usuario", {}, ["creado_en", "birthdate"], False),
    ("categorias", Categoria, "Categoria.json", "Categoria", {"image": "imagen"}, [], False),
    ("productos", Producto, "Producto.json", "Producto", {}, ["creado_en"], False),
    ("producto_imagenes", ProductoImagen, "Producto.json", "ProductoImagen", {}, [], True),
    ("producto_atributos", ProductoAtributo, "Producto.json", "ProductoAtributo", {}, [], True),
    ("amistades", Amistad, "Usuario.json", "Amistad", {}, ["creado_en"], False),
    ("eventos", Evento, "Evento.json", "Evento", {}, ["fecha", "creado_en"], False),
    ("evento_asistentes", EventoAsistente, "Evento.json", "EventoAsistente", {}, ["creado_en"], False),
    ("reviews", Review, "Review.json", "Review", {}, ["creado_en"], False),
    ("compartidos", Compartido, "Compartido.json", "Compartido", {}, ["creado_en"], False),
    ("highlights", Highlight, "Highlight.json", "Highlights", {}, ["creado_en"], False),
]

# Orden inverso para el borrado (hijos antes que padres).
TABLAS_EN_ORDEN = [p[0] for p in PLAN]


def _vaciar_tablas(session):
    """Vacía las tablas del PLAN respetando FKs (desactiva checks temporalmente
    solo dentro de la transacción; no cambia configuración global del servidor)."""
    session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for tabla in reversed(TABLAS_EN_ORDEN):
        session.execute(text(f"DELETE FROM {tabla}"))
    session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))


def cargar(verbose: bool = True):
    handler = ManejadorBD()
    handler.crear_bd()  # asegura que el esquema exista

    Session = handler.getSesion()
    session = Session()
    resumen = {}
    try:
        _vaciar_tablas(session)

        for tabla, modelo, archivo, clave, mapeo, fechas, descartar_id in PLAN:
            data = _leer_json(archivo)
            filas = data.get(clave, [])
            registros = [
                _filtrar_columnas(modelo, fila, mapeo, fechas) for fila in filas
            ]

            if descartar_id:
                # Dejar autoincrement: se ignora el id del JSON.
                for reg in registros:
                    reg.pop("id", None)
                unicos = registros
            else:
                # Deduplicar por id para evitar violaciones de PK.
                vistos = set()
                unicos = []
                for reg in registros:
                    rid = reg.get("id")
                    if rid is not None and rid in vistos:
                        continue
                    if rid is not None:
                        vistos.add(rid)
                    unicos.append(reg)

            if unicos:
                session.execute(modelo.__table__.insert(), unicos)
            resumen[tabla] = len(unicos)
            if verbose:
                print(f"  {tabla}: {len(unicos)} filas")

        session.commit()
        if verbose:
            print("Migración de datos semilla completada.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    return resumen


if __name__ == "__main__":
    cargar()
