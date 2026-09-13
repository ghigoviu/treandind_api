"""
Configuración de pytest para la API de Treanding.

Apunta la aplicación a la base de datos de pruebas `treanding_test`
(localhost:3306, root sin contraseña) mediante variables de entorno, ANTES de
importar cualquier módulo de la app (Config usa lru_cache y ManejadorBD es un
Singleton, por lo que el entorno debe fijarse primero).

Cada test corre dentro de una transacción que se revierte al finalizar, dejando
la BD de pruebas limpia entre tests. NO se toca la BD de desarrollo ni la
configuración del servidor MySQL.
"""
import os

# --- Debe ejecutarse antes de importar la app ---------------------------------
os.environ.setdefault("MYSQL_USER", "root")
os.environ.setdefault("MYSQL_PASSWORD", "")
os.environ.setdefault("MYSQL_HOST", "localhost")
os.environ.setdefault("MYSQL_PORT", "3306")
os.environ.setdefault("MYSQL_DB", "treanding_test")
os.environ.setdefault("SQL_ECHO", "false")

import pytest
from fastapi.testclient import TestClient

# Importar la app y la infraestructura de BD (ya con el entorno de test fijado).
from ControladorRest.Router import app
from ControladorRest import get_db
from Datos.ManejadorBD import ManejadorBD


@pytest.fixture(scope="session", autouse=True)
def _crear_esquema():
    """Crea el esquema en treanding_test una vez por sesión de tests."""
    handler = ManejadorBD()
    # Salvaguarda: nunca crear el esquema fuera de una BD de pruebas.
    url = str(handler.getEngine().url)
    assert "treanding_test" in url, (
        f"Los tests deben apuntar a treanding_test, no a: {url}"
    )
    handler.crear_bd()
    yield


@pytest.fixture()
def db_session():
    """Sesión transaccional por test con SAVEPOINTs anidados.

    El código de la aplicación (repos) hace `commit()`; para que eso no confirme
    la transacción externa del test, usamos un SAVEPOINT que se reinicia
    automáticamente tras cada commit interno. Al final se revierte todo, dejando
    treanding_test limpia entre tests.
    """
    from sqlalchemy import event

    handler = ManejadorBD()
    engine = handler.getEngine()
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = handler.getSesion()
    session = SessionLocal(bind=connection, join_transaction_mode="create_savepoint")

    # Reiniciar el SAVEPOINT cada vez que el código haga commit del anidado.
    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def _restart_savepoint(sess, trans):
        nonlocal nested
        if trans.nested and not trans._parent.nested:
            if connection.in_transaction():
                nested = connection.begin_nested()

    try:
        yield session
    finally:
        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    """TestClient con get_db sobreescrito para usar la sesión transaccional."""
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
