"""
Tests de Amistades y Compartidos:
- No auto-amistad, no duplicado en sentido inverso.
- Transición de estado pendiente -> aceptada.
- Listar amigos y pendientes.
- Compartir con amigo en sentido inverso funciona; con no-amigo -> 403.
"""
from sqlalchemy import text


def _usuario(db_session, email):
    r = db_session.execute(
        text("INSERT INTO usuarios (nombre, email, password, creado_en) "
             "VALUES ('U', :email, 'x', NOW())"),
        {"email": email},
    )
    db_session.flush()
    return r.lastrowid


def _producto(db_session):
    r = db_session.execute(
        text("INSERT INTO productos (nombre, slug, precio, stock, img_portada, "
             "creado_en, requiere_edad, calificacion) VALUES ('P','p',10,5,'',NOW(),0,0)")
    )
    db_session.flush()
    return r.lastrowid


# --- Amistades ---------------------------------------------------------------

def test_no_auto_amistad(client, db_session):
    u = _usuario(db_session, "a1@test.com")
    r = client.post("/amistades/", json={"usuario_id": u, "amigo_id": u})
    assert r.status_code == 400, r.text


def test_no_duplicado_sentido_inverso(client, db_session):
    a = _usuario(db_session, "a2@test.com")
    b = _usuario(db_session, "b2@test.com")

    r1 = client.post("/amistades/", json={"usuario_id": a, "amigo_id": b})
    assert r1.status_code == 201, r1.text

    # Intentar en sentido inverso -> rechazado (ya existe).
    r2 = client.post("/amistades/", json={"usuario_id": b, "amigo_id": a})
    assert r2.status_code == 400, r2.text


def test_transicion_estado_y_listados(client, db_session):
    a = _usuario(db_session, "a3@test.com")
    b = _usuario(db_session, "b3@test.com")

    r = client.post("/amistades/", json={"usuario_id": a, "amigo_id": b})
    amistad_id = r.json()["id"]

    # b tiene una solicitud pendiente recibida.
    pend = client.get(f"/amistades/usuario/{b}/pendientes")
    assert pend.status_code == 200
    assert any(x["id"] == amistad_id for x in pend.json())

    # Aceptar.
    upd = client.patch(f"/amistades/{amistad_id}/estado", json={"estado": "aceptada"})
    assert upd.status_code == 200, upd.text

    # Ahora aparece en amigos de ambos.
    amigos_a = client.get(f"/amistades/usuario/{a}").json()
    amigos_b = client.get(f"/amistades/usuario/{b}").json()
    assert any(x["id"] == amistad_id for x in amigos_a)
    assert any(x["id"] == amistad_id for x in amigos_b)


# --- Compartidos -------------------------------------------------------------

def test_compartir_con_amigo_sentido_inverso(client, db_session):
    a = _usuario(db_session, "c1@test.com")
    b = _usuario(db_session, "c1b@test.com")
    pid = _producto(db_session)

    # Amistad a -> b.
    client.post("/amistades/", json={"usuario_id": a, "amigo_id": b})

    # b comparte con a (sentido inverso a la amistad): debe funcionar.
    r = client.post("/compartidos/", json={
        "usuario_id": b, "amigo_id": a, "producto_id": pid, "mensaje": "Mira"})
    assert r.status_code == 201, r.text


def test_compartir_con_no_amigo_403(client, db_session):
    a = _usuario(db_session, "c2@test.com")
    extrano = _usuario(db_session, "c2x@test.com")
    pid = _producto(db_session)

    r = client.post("/compartidos/", json={
        "usuario_id": a, "amigo_id": extrano, "producto_id": pid})
    assert r.status_code == 403, r.text


def test_compartir_consigo_mismo_400(client, db_session):
    a = _usuario(db_session, "c3@test.com")
    pid = _producto(db_session)
    r = client.post("/compartidos/", json={"usuario_id": a, "amigo_id": a, "producto_id": pid})
    assert r.status_code == 400, r.text
