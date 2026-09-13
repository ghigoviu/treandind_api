"""
Tests de publicación de productos: solo vendedor validado publica,
tipo (fisico/servicio/evento), atributos (3 tabs), inventario.
"""
from sqlalchemy import text


def _usuario(db_session, email, tipo='vendedor'):
    r = db_session.execute(
        text("INSERT INTO usuarios (nombre, email, password, tipo_perfil, creado_en) "
             "VALUES ('U', :email, 'x', :tipo, NOW())"),
        {"email": email, "tipo": tipo},
    )
    db_session.flush()
    return r.lastrowid


def _validar_vendedor(client, uid):
    return client.post("/perfil-vendedor/", json={
        "usuario_id": uid,
        "metodos_entrega": "E", "lugares_entrega": "L",
        "info_general": "I", "datos_bancarios": "D",
    })


def test_vendedor_validado_publica(client, db_session):
    uid = _usuario(db_session, "pub1@test.com", "vendedor")
    _validar_vendedor(client, uid)

    resp = client.post("/productos/", json={
        "nombre": "Camiseta", "precio": 100, "stock": 10, "tipo": "fisico",
        "descripcion": "Algodón", "usuario_id": uid,
        "atributos": [
            {"nombre": "Talla", "valor": "M"},
            {"nombre": "Color", "valor": "Azul"},
            {"nombre": "Material", "valor": "Algodón"},
        ],
    })
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["tipo"] == "fisico"
    assert data["stock"] == 10


def test_vendedor_no_validado_no_publica_403(client, db_session):
    uid = _usuario(db_session, "pub2@test.com", "vendedor")
    # NO validar

    resp = client.post("/productos/", json={
        "nombre": "X", "precio": 10, "usuario_id": uid,
    })
    assert resp.status_code == 403, resp.text


def test_visitante_no_publica_403(client, db_session):
    uid = _usuario(db_session, "pub3@test.com", "visitante")

    resp = client.post("/productos/", json={
        "nombre": "X", "precio": 10, "usuario_id": uid,
    })
    assert resp.status_code == 403, resp.text


def test_tipo_servicio(client, db_session):
    uid = _usuario(db_session, "pub4@test.com", "influencer")
    _validar_vendedor(client, uid)

    resp = client.post("/productos/", json={
        "nombre": "Consultoría", "precio": 500, "tipo": "servicio", "usuario_id": uid,
    })
    assert resp.status_code == 200, resp.text
    assert resp.json()["tipo"] == "servicio"


def test_tipo_invalido_422(client, db_session):
    uid = _usuario(db_session, "pub5@test.com", "vendedor")
    _validar_vendedor(client, uid)

    resp = client.post("/productos/", json={
        "nombre": "X", "precio": 10, "tipo": "raro", "usuario_id": uid,
    })
    assert resp.status_code == 422, resp.text


def test_atributos_persistidos(client, db_session):
    uid = _usuario(db_session, "pub6@test.com", "vendedor")
    _validar_vendedor(client, uid)

    r = client.post("/productos/", json={
        "nombre": "Tenis", "precio": 200, "usuario_id": uid,
        "atributos": [{"nombre": "Detalles", "valor": "Edición limitada"}],
    })
    pid = r.json()["id"]

    det = client.get(f"/productos/id/{pid}")
    assert det.status_code == 200
    assert det.json()["tipo"] == "fisico"
    assert len(det.json()["atributos"]) >= 1
