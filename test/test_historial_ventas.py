"""
Tests de historial de compras (por usuario), ventas (por vendedor) y productos
publicados por vendedor.
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


def _producto(db_session, vendedor_id, nombre="P", oculto=0):
    r = db_session.execute(
        text("INSERT INTO productos (nombre, slug, precio, stock, tipo, oculto, img_portada, "
             "creado_en, requiere_edad, calificacion, usuario_id) "
             "VALUES (:n, 'p', 100, 5, 'fisico', :oc, '', NOW(), 0, 0, :uid)"),
        {"n": nombre, "oc": oculto, "uid": vendedor_id},
    )
    db_session.flush()
    return r.lastrowid


def _orden(db_session, comprador_id, producto_id, cantidad=1, precio=100):
    ro = db_session.execute(
        text("INSERT INTO ordenes (estado, total, creado_en, usuario_id) "
             "VALUES ('completada', :total, NOW(), :uid)"),
        {"total": cantidad * precio, "uid": comprador_id},
    )
    db_session.flush()
    orden_id = ro.lastrowid
    db_session.execute(
        text("INSERT INTO orden_detalles (cantidad, precio_unit, orden_id, producto_id) "
             "VALUES (:c, :p, :oid, :pid)"),
        {"c": cantidad, "p": precio, "oid": orden_id, "pid": producto_id},
    )
    db_session.flush()
    return orden_id


def test_historial_compras_por_usuario(client, db_session):
    vendedor = _usuario(db_session, "hv1v@test.com")
    comprador = _usuario(db_session, "hv1c@test.com", "visitante")
    pid = _producto(db_session, vendedor)
    _orden(db_session, comprador, pid)
    _orden(db_session, comprador, pid)

    r = client.get(f"/ordenes/usuario/{comprador}")
    assert r.status_code == 200, r.text
    assert len(r.json()) == 2
    assert all(o["usuario_id"] == comprador for o in r.json())


def test_ventas_por_vendedor(client, db_session):
    vendedor = _usuario(db_session, "hv2v@test.com")
    comprador = _usuario(db_session, "hv2c@test.com", "visitante")
    pid = _producto(db_session, vendedor, "Zapatos")
    _orden(db_session, comprador, pid, cantidad=2, precio=150)

    r = client.get(f"/ordenes/vendedor/{vendedor}/ventas")
    assert r.status_code == 200, r.text
    ventas = r.json()
    assert len(ventas) == 1
    assert ventas[0]["producto_nombre"] == "Zapatos"
    assert ventas[0]["cantidad"] == 2
    assert ventas[0]["subtotal"] == 300


def test_productos_por_vendedor_incluye_ocultos(client, db_session):
    vendedor = _usuario(db_session, "hv3v@test.com")
    _producto(db_session, vendedor, "Visible", oculto=0)
    _producto(db_session, vendedor, "Oculto", oculto=1)

    r = client.get(f"/productos/vendedor/{vendedor}")
    assert r.status_code == 200, r.text
    nombres = [p["nombre"] for p in r.json()]
    assert "Visible" in nombres
    assert "Oculto" in nombres  # el dueño ve también los ocultos


def test_detalles_orden(client, db_session):
    vendedor = _usuario(db_session, "hv4v@test.com")
    comprador = _usuario(db_session, "hv4c@test.com", "visitante")
    pid = _producto(db_session, vendedor)
    oid = _orden(db_session, comprador, pid, cantidad=3, precio=50)

    r = client.get(f"/ordenes/{oid}/detalles")
    assert r.status_code == 200, r.text
    assert len(r.json()) == 1
    assert r.json()[0]["cantidad"] == 3
    assert r.json()[0]["precio_unit"] == 50
