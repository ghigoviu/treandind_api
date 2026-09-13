"""
Tests del calendario: eventos suscritos por usuario y eventos por vendedor.
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


def _evento(client, vendedor_id, nombre, boletos=10):
    return client.post("/eventos/", json={
        "usuario_id": vendedor_id, "nombre": nombre, "precio": 100,
        "categoria": "Evento", "fecha": "2026-12-01T20:00:00",
        "ubicacion": "CDMX", "boletos_total": boletos,
    }).json()["id"]


def test_eventos_suscritos(client, db_session):
    vendedor = _usuario(db_session, "cal1v@test.com")
    visitante = _usuario(db_session, "cal1c@test.com", "visitante")

    ev1 = _evento(client, vendedor, "Concierto")
    ev2 = _evento(client, vendedor, "Taller")
    _evento(client, vendedor, "NoSuscrito")

    # El visitante se suscribe a 2 eventos.
    client.post(f"/eventos/{ev1}/registrar-asistente", json={"usuario_id": visitante})
    client.post(f"/eventos/{ev2}/registrar-asistente", json={"usuario_id": visitante})

    suscritos = client.get(f"/eventos/usuario/{visitante}/suscritos").json()
    ids = [e["id"] for e in suscritos]
    assert ev1 in ids
    assert ev2 in ids
    assert len(suscritos) == 2


def test_eventos_del_vendedor_para_calendario(client, db_session):
    vendedor = _usuario(db_session, "cal2v@test.com")
    _evento(client, vendedor, "E1")
    _evento(client, vendedor, "E2")

    r = client.get(f"/eventos/vendedor/{vendedor}")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_suscritos_vacio(client, db_session):
    visitante = _usuario(db_session, "cal3@test.com", "visitante")
    r = client.get(f"/eventos/usuario/{visitante}/suscritos")
    assert r.status_code == 200
    assert r.json() == []
