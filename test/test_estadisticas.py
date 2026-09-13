"""
Tests de estadísticas de ventas del vendedor: totales, top productos,
top compradores, ventas por mes.
"""
from sqlalchemy import text


def _usuario(db_session, email, tipo='vendedor'):
    r = db_session.execute(
        text("INSERT INTO usuarios (nombre, email, password, tipo_perfil, creado_en) "
             "VALUES (:e, :email, 'x', :tipo, NOW())"),
        {"e": email.split("@")[0], "email": email, "tipo": tipo},
    )
    db_session.flush()
    return r.lastrowid


def _producto(db_session, vendedor_id, nombre, precio=100):
    r = db_session.execute(
        text("INSERT INTO productos (nombre, slug, precio, stock, tipo, oculto, img_portada, "
             "creado_en, requiere_edad, calificacion, usuario_id) "
             "VALUES (:n, 'p', :precio, 100, 'fisico', 0, '', NOW(), 0, 0, :uid)"),
        {"n": nombre, "precio": precio, "uid": vendedor_id},
    )
    db_session.flush()
    return r.lastrowid


def _orden(db_session, comprador_id, producto_id, cantidad, precio):
    ro = db_session.execute(
        text("INSERT INTO ordenes (estado, total, creado_en, usuario_id) "
             "VALUES ('completada', :total, NOW(), :uid)"),
        {"total": cantidad * precio, "uid": comprador_id},
    )
    db_session.flush()
    db_session.execute(
        text("INSERT INTO orden_detalles (cantidad, precio_unit, orden_id, producto_id) "
             "VALUES (:c, :p, :oid, :pid)"),
        {"c": cantidad, "p": precio, "oid": ro.lastrowid, "pid": producto_id},
    )
    db_session.flush()


def test_resumen_totales(client, db_session):
    vendedor = _usuario(db_session, "est1v@test.com")
    comprador = _usuario(db_session, "est1c@test.com", "visitante")
    p1 = _producto(db_session, vendedor, "Camisa", 100)
    p2 = _producto(db_session, vendedor, "Gorra", 50)

    _orden(db_session, comprador, p1, 2, 100)  # 200
    _orden(db_session, comprador, p2, 1, 50)   # 50

    r = client.get(f"/estadisticas/vendedor/{vendedor}")
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["total_ventas"] == 2
    assert data["total_ingresos"] == 250.0
    assert data["unidades_vendidas"] == 3


def test_top_productos_y_compradores(client, db_session):
    vendedor = _usuario(db_session, "est2v@test.com")
    c1 = _usuario(db_session, "est2c1@test.com", "visitante")
    c2 = _usuario(db_session, "est2c2@test.com", "visitante")
    p1 = _producto(db_session, vendedor, "Popular", 100)
    p2 = _producto(db_session, vendedor, "Menos", 100)

    # p1 se vende más unidades.
    _orden(db_session, c1, p1, 5, 100)
    _orden(db_session, c2, p2, 1, 100)
    # c1 compra más veces.
    _orden(db_session, c1, p2, 1, 100)

    data = client.get(f"/estadisticas/vendedor/{vendedor}").json()

    # Top producto por unidades = Popular.
    assert data["top_productos"][0]["nombre"] == "Popular"
    # Top comprador = c1 (2 compras).
    assert data["top_compradores"][0]["usuario_id"] == c1
    assert data["top_compradores"][0]["compras"] == 2


def test_ventas_por_mes(client, db_session):
    vendedor = _usuario(db_session, "est3v@test.com")
    comprador = _usuario(db_session, "est3c@test.com", "visitante")
    p1 = _producto(db_session, vendedor, "X", 30)

    _orden(db_session, comprador, p1, 1, 30)

    data = client.get(f"/estadisticas/vendedor/{vendedor}").json()
    assert len(data["ventas_por_mes"]) >= 1
    assert data["ventas_por_mes"][0]["ventas"] >= 1


def test_vendedor_sin_ventas(client, db_session):
    vendedor = _usuario(db_session, "est4v@test.com")
    data = client.get(f"/estadisticas/vendedor/{vendedor}").json()
    assert data["total_ventas"] == 0
    assert data["total_ingresos"] == 0.0
    assert data["top_productos"] == []
