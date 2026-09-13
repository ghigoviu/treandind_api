"""
Tests de Colaboración / Página Social: CRUD, solo vendedor crea, invitación con
porcentaje, aceptar/replicar, publicar bloqueado hasta que todos acepten.
"""
from sqlalchemy import text


def _crear_usuario(db_session, nombre, email, tipo='vendedor'):
    result = db_session.execute(
        text("INSERT INTO usuarios (nombre, email, password, tipo_perfil, creado_en) "
             "VALUES (:nombre, :email, 'x', :tipo, NOW())"),
        {"nombre": nombre, "email": email, "tipo": tipo},
    )
    db_session.flush()
    return result.lastrowid


def test_crud_colaboracion(client, db_session):
    uid = _crear_usuario(db_session, "Creador", "creador@test.com", "vendedor")

    resp = client.post("/colaboracion/", json={
        "desc": "Colaboración de prueba",
        "nombre_comercial": "Mi Tienda",
        "img": "http://img",
        "usuario_id": uid,
    })
    assert resp.status_code == 201, resp.text
    creada = resp.json()
    assert creada["desc"] == "Colaboración de prueba"
    assert creada["usuario_id"] == uid
    colaboracion_id = creada["id"]

    # Listar / obtener
    assert any(c["id"] == colaboracion_id for c in client.get("/colaboracion/").json())
    assert client.get(f"/colaboracion/{colaboracion_id}").status_code == 200

    # Actualizar
    resp = client.put(f"/colaboracion/{colaboracion_id}", json={"desc": "Actualizada"})
    assert resp.status_code == 200
    assert resp.json()["desc"] == "Actualizada"

    # Borrar
    assert client.delete(f"/colaboracion/{colaboracion_id}").status_code == 200
    assert client.get(f"/colaboracion/{colaboracion_id}").status_code == 404


def test_solo_vendedor_crea_pagina(client, db_session):
    visitante = _crear_usuario(db_session, "Vis", "vis@test.com", "visitante")
    resp = client.post("/colaboracion/", json={"desc": "X", "usuario_id": visitante})
    assert resp.status_code == 403, resp.text


def test_invitar_y_aceptar(client, db_session):
    creador = _crear_usuario(db_session, "Creador2", "creador2@test.com", "vendedor")
    amigo = _crear_usuario(db_session, "Amigo", "amigo@test.com", "vendedor")

    cid = client.post("/colaboracion/", json={
        "desc": "Con miembros", "nombre_comercial": "Colab", "usuario_id": creador
    }).json()["id"]

    # Al crear, la página aún puede publicar (solo el creador, ya aceptado).
    assert client.get(f"/colaboracion/{cid}/puede-publicar").json()["puede_publicar"] is True

    # Invitar con 30% sugerido.
    resp = client.post(f"/colaboracion/{cid}/invitar",
                       json={"usuario_id": amigo, "porcentaje_sugerido": 30})
    assert resp.status_code == 201, resp.text
    assert resp.json()["estado"] == "pendiente"

    # Ahora hay un pendiente -> no puede publicar.
    assert client.get(f"/colaboracion/{cid}/puede-publicar").json()["puede_publicar"] is False

    # Se generó notificación de invitación al amigo.
    notifs = client.get(f"/notificaciones/usuario/{amigo}").json()
    assert any(n["tipo"] == "invitacion" for n in notifs)

    # El amigo acepta el % sugerido.
    resp = client.post(f"/colaboracion/{cid}/responder/{amigo}", json={"accion": "aceptar"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["estado"] == "aceptada"
    assert resp.json()["porcentaje"] == 30

    # Todos aceptaron -> puede publicar de nuevo.
    assert client.get(f"/colaboracion/{cid}/puede-publicar").json()["puede_publicar"] is True


def test_replicar_porcentaje(client, db_session):
    creador = _crear_usuario(db_session, "C3", "c3@test.com", "vendedor")
    amigo = _crear_usuario(db_session, "A3", "a3@test.com", "vendedor")

    cid = client.post("/colaboracion/", json={"desc": "R", "usuario_id": creador}).json()["id"]
    client.post(f"/colaboracion/{cid}/invitar", json={"usuario_id": amigo, "porcentaje_sugerido": 20})

    # El amigo replica proponiendo 45%.
    resp = client.post(f"/colaboracion/{cid}/responder/{amigo}",
                       json={"accion": "replicar", "porcentaje": 45})
    assert resp.status_code == 200, resp.text
    assert resp.json()["estado"] == "replicada"
    assert resp.json()["porcentaje"] == 45


def test_invitar_duplicado_400(client, db_session):
    creador = _crear_usuario(db_session, "C4", "c4@test.com", "vendedor")
    amigo = _crear_usuario(db_session, "A4", "a4@test.com", "vendedor")

    cid = client.post("/colaboracion/", json={"desc": "D", "usuario_id": creador}).json()["id"]
    r1 = client.post(f"/colaboracion/{cid}/invitar", json={"usuario_id": amigo, "porcentaje_sugerido": 10})
    assert r1.status_code == 201
    r2 = client.post(f"/colaboracion/{cid}/invitar", json={"usuario_id": amigo, "porcentaje_sugerido": 5})
    assert r2.status_code == 400


def test_detalle_incluye_miembros_y_estado(client, db_session):
    creador = _crear_usuario(db_session, "C5", "c5@test.com", "vendedor")
    amigo = _crear_usuario(db_session, "A5", "a5@test.com", "vendedor")

    cid = client.post("/colaboracion/", json={
        "desc": "Det", "nombre_comercial": "Marca X", "usuario_id": creador
    }).json()["id"]
    client.post(f"/colaboracion/{cid}/invitar", json={"usuario_id": amigo, "porcentaje_sugerido": 25})

    det = client.get(f"/colaboracion/{cid}/detalle").json()
    assert det["nombre_comercial"] == "Marca X"
    assert det["puede_publicar"] is False  # amigo pendiente
    # El creador (aceptado) y el amigo (pendiente) están en miembros.
    estados = {m["usuario_id"]: m["estado"] for m in det["miembros"]}
    assert estados[creador] == "aceptada"
    assert estados[amigo] == "pendiente"
