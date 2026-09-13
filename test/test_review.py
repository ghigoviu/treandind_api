"""
Tests de Reviews: validación de rango 1-5, anti-duplicado por usuario+item,
y recálculo de promedio atómico (incluida la última review sin crash).
"""
from sqlalchemy import text


def _crear_usuario(db_session, email):
    r = db_session.execute(
        text("INSERT INTO usuarios (nombre, email, password, creado_en) "
             "VALUES ('U', :email, 'x', NOW())"),
        {"email": email},
    )
    db_session.flush()
    return r.lastrowid


def _crear_producto(db_session, nombre="Prod"):
    r = db_session.execute(
        text("INSERT INTO productos (nombre, slug, precio, stock, img_portada, "
             "creado_en, requiere_edad, calificacion) "
             "VALUES (:n, :n, 10, 5, '', NOW(), 0, 0)"),
        {"n": nombre},
    )
    db_session.flush()
    return r.lastrowid


def _crear_evento(db_session, usuario_id, nombre="Evt"):
    r = db_session.execute(
        text("INSERT INTO eventos (usuario_id, nombre, precio, categoria, fecha, "
             "ubicacion, calificacion, creado_en) "
             "VALUES (:u, :n, 20, 'Evento', NOW(), 'Aqui', 0, NOW())"),
        {"u": usuario_id, "n": nombre},
    )
    db_session.flush()
    return r.lastrowid


def _registrar_compra(db_session, usuario_id, producto_id):
    """Inserta una orden completada con el producto, para habilitar la reseña."""
    ro = db_session.execute(
        text("INSERT INTO ordenes (estado, total, creado_en, usuario_id) "
             "VALUES ('completada', 10, NOW(), :uid)"),
        {"uid": usuario_id},
    )
    db_session.flush()
    db_session.execute(
        text("INSERT INTO orden_detalles (cantidad, precio_unit, orden_id, producto_id) "
             "VALUES (1, 10, :oid, :pid)"),
        {"oid": ro.lastrowid, "pid": producto_id},
    )
    db_session.flush()


def test_crear_review_actualiza_promedio(client, db_session):
    uid = _crear_usuario(db_session, "rev1@test.com")
    pid = _crear_producto(db_session)
    _registrar_compra(db_session, uid, pid)

    resp = client.post("/reviews/", json={
        "usuario_id": uid, "producto_id": pid, "calificacion": 4, "comentario": "Bien"})
    assert resp.status_code == 201, resp.text

    # El promedio del producto se actualizó.
    fila = db_session.execute(
        text("SELECT calificacion FROM productos WHERE id = :id"), {"id": pid}
    ).first()
    assert fila[0] == 4.0


def test_calificacion_fuera_de_rango_422(client, db_session):
    uid = _crear_usuario(db_session, "rev2@test.com")
    pid = _crear_producto(db_session)

    for mala in (0, 6, -1, 10):
        resp = client.post("/reviews/", json={
            "usuario_id": uid, "producto_id": pid, "calificacion": mala})
        assert resp.status_code == 422, f"cal={mala}: {resp.text}"


def test_review_duplicada_del_mismo_usuario_409(client, db_session):
    uid = _crear_usuario(db_session, "rev3@test.com")
    pid = _crear_producto(db_session)
    _registrar_compra(db_session, uid, pid)

    r1 = client.post("/reviews/", json={"usuario_id": uid, "producto_id": pid, "calificacion": 5})
    assert r1.status_code == 201, r1.text

    r2 = client.post("/reviews/", json={"usuario_id": uid, "producto_id": pid, "calificacion": 3})
    assert r2.status_code == 409, r2.text


def test_review_requiere_exactamente_un_item(client, db_session):
    uid = _crear_usuario(db_session, "rev4@test.com")
    pid = _crear_producto(db_session)
    eid = _crear_evento(db_session, uid)

    # Ni producto ni evento -> 400
    r = client.post("/reviews/", json={"usuario_id": uid, "calificacion": 4})
    assert r.status_code == 400, r.text

    # Ambos -> 400
    r = client.post("/reviews/", json={
        "usuario_id": uid, "producto_id": pid, "evento_id": eid, "calificacion": 4})
    assert r.status_code == 400, r.text


def test_borrar_ultima_review_recalcula_sin_crash(client, db_session):
    autor = _crear_usuario(db_session, "rev5@test.com")
    otro = _crear_usuario(db_session, "rev5b@test.com")
    pid = _crear_producto(db_session)
    _registrar_compra(db_session, autor, pid)
    _registrar_compra(db_session, otro, pid)

    # Dos reviews de usuarios distintos.
    r1 = client.post("/reviews/", json={"usuario_id": autor, "producto_id": pid, "calificacion": 5})
    r2 = client.post("/reviews/", json={"usuario_id": otro, "producto_id": pid, "calificacion": 3})
    assert r1.status_code == 201 and r2.status_code == 201
    review1_id = r1.json()["id"]

    # Promedio = 4.0
    prom = db_session.execute(text("SELECT calificacion FROM productos WHERE id=:id"), {"id": pid}).first()[0]
    assert prom == 4.0

    # Borrar una review -> promedio = 3.0
    d = client.delete(f"/reviews/{review1_id}/usuario/{autor}")
    assert d.status_code == 200, d.text
    prom = db_session.execute(text("SELECT calificacion FROM productos WHERE id=:id"), {"id": pid}).first()[0]
    assert prom == 3.0

    # Borrar la última review -> promedio = 0.0 sin crash
    r3 = db_session.execute(text("SELECT id FROM reviews WHERE producto_id=:id"), {"id": pid}).first()
    d = client.delete(f"/reviews/{r3[0]}/usuario/{otro}")
    assert d.status_code == 200, d.text
    prom = db_session.execute(text("SELECT calificacion FROM productos WHERE id=:id"), {"id": pid}).first()[0]
    assert prom == 0.0


def test_borrar_review_de_otro_usuario_403(client, db_session):
    autor = _crear_usuario(db_session, "rev6@test.com")
    intruso = _crear_usuario(db_session, "rev6b@test.com")
    pid = _crear_producto(db_session)
    _registrar_compra(db_session, autor, pid)

    r = client.post("/reviews/", json={"usuario_id": autor, "producto_id": pid, "calificacion": 5})
    review_id = r.json()["id"]

    d = client.delete(f"/reviews/{review_id}/usuario/{intruso}")
    assert d.status_code == 403, d.text


def test_resenar_sin_comprar_403(client, db_session):
    uid = _crear_usuario(db_session, "rev7@test.com")
    pid = _crear_producto(db_session)
    # NO se registra compra.

    r = client.post("/reviews/", json={"usuario_id": uid, "producto_id": pid, "calificacion": 5})
    assert r.status_code == 403, r.text


def test_resenar_tras_comprar_ok(client, db_session):
    uid = _crear_usuario(db_session, "rev8@test.com")
    pid = _crear_producto(db_session)
    _registrar_compra(db_session, uid, pid)

    r = client.post("/reviews/", json={"usuario_id": uid, "producto_id": pid, "calificacion": 4})
    assert r.status_code == 201, r.text
