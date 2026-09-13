"""
Smoke tests: validan que la app arranca contra treanding_test, que el esquema
se creó y que get_db entrega una sesión válida.
"""


def test_get_usuarios_responde_200(client):
    resp = client.get("/usuarios/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_get_productos_responde_200(client):
    resp = client.get("/productos/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_esquema_creado_en_treanding_test(db_session):
    """Verifica que la sesión de test apunta a treanding_test y que las tablas
    principales existen (consultables sin error)."""
    from sqlalchemy import text

    url = str(db_session.get_bind().engine.url)
    assert "treanding_test" in url

    # Si el esquema no existiera, estas consultas lanzarían error.
    for tabla in ("usuarios", "productos", "amistades", "reviews", "compartidos", "colaboracion"):
        db_session.execute(text(f"SELECT COUNT(*) FROM {tabla}"))
