"""
Tests de eventos con boletos: crear con boletos, registrar asistente decrementa
disponibles, sin boletos no se registra, eventos por vendedor.
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


def test_crear_evento_con_boletos(client, db_session):
    uid = _usuario(db_session, "ev1@test.com")
    resp = client.post("/eventos/", json={
        "usuario_id": uid, "nombre": "Concierto", "precio": 100,
        "categoria": "Evento", "fecha": "2026-12-01T20:00:00",
        "ubicacion": "Arena CDMX", "img_flyer": "http://flyer.jpg",
        "boletos_total": 100,
    })
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["boletos_total"] == 100
    assert data["boletos_disponibles"] == 100


def test_registrar_asistente_decrementa_boletos(client, db_session):
    uid = _usuario(db_session, "ev2@test.com")
    asistente = _usuario(db_session, "ev2a@test.com", "visitante")

    r = client.post("/eventos/", json={
        "usuario_id": uid, "nombre": "Taller", "precio": 50,
        "categoria": "Evento", "fecha": "2026-11-01T10:00:00",
        "ubicacion": "Online", "boletos_total": 2,
    })
    evento_id = r.json()["id"]

    reg = client.post(f"/eventos/{evento_id}/registrar-asistente", json={"usuario_id": asistente})
    assert reg.status_code == 200, reg.text

    det = client.get(f"/eventos/{evento_id}")
    assert det.json()["boletos_disponibles"] == 1


def test_sin_boletos_no_registra(client, db_session):
    uid = _usuario(db_session, "ev3@test.com")
    a1 = _usuario(db_session, "ev3a@test.com", "visitante")

    r = client.post("/eventos/", json={
        "usuario_id": uid, "nombre": "Exclusivo", "precio": 500,
        "categoria": "Evento", "fecha": "2026-10-01T18:00:00",
        "ubicacion": "VIP", "boletos_total": 1,
    })
    evento_id = r.json()["id"]

    # Primer asistente ocupa el único boleto.
    r1 = client.post(f"/eventos/{evento_id}/registrar-asistente", json={"usuario_id": a1})
    assert r1.status_code == 200

    # Segundo asistente: sin boletos -> 400.
    a2 = _usuario(db_session, "ev3b@test.com", "visitante")
    r2 = client.post(f"/eventos/{evento_id}/registrar-asistente", json={"usuario_id": a2})
    assert r2.status_code == 400, r2.text


def test_eventos_por_vendedor(client, db_session):
    uid = _usuario(db_session, "ev4@test.com")
    for i in range(2):
        client.post("/eventos/", json={
            "usuario_id": uid, "nombre": f"E{i}", "precio": 10,
            "categoria": "Evento", "fecha": "2026-09-01T12:00:00",
            "ubicacion": "X", "boletos_total": 5,
        })

    r = client.get(f"/eventos/vendedor/{uid}")
    assert r.status_code == 200
    assert len(r.json()) == 2
