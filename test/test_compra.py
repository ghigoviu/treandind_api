"""
Tests del flujo de compra: crea orden, descuenta stock, valida stock
insuficiente, producto oculto no comprable, aparece en historial.
"""
from sqlalchemy import text


def _usuario(db_session, email, tipo='visitante'):
    r = db_session.execute(
        text("INSERT INTO usuarios (nombre, email, password, tipo_perfil, creado_en) "
             "VALUES ('U', :email, 'x', :tipo, NOW())"),
        {"email": email, "tipo": tipo},
    )
    db_session.flush()
    return r.lastrowid


def _producto(db_session, vendedor_id, precio=100, stock=10, oculto=0):
    r = db_session.execute(
        text("INSERT INTO productos (nombre, slug, precio, stock, tipo, oculto, img_portada, "
             "creado_en, requiere_edad, calificacion, usuario_id) "
             "VALUES ('P', 'p', :precio, :stock, 'fisico', :oc, '', NOW(), 0, 0, :uid)"),
        {"precio": precio, "stock": stock, "oc": oculto, "uid": vendedor_id},
    )
    db_session.flush()
    return r.lastrowid


def test_comprar_descuenta_stock(client, db_session):
    vendedor = _usuario(db_session, "cmp1v@test.com", "vendedor")
    comprador = _usuario(db_session, "cmp1c@test.com")
    pid = _producto(db_session, vendedor, precio=50, stock=10)

    r = client.post("/ordenes/comprar", json={
        "usuario_id": comprador, "producto_id": pid, "cantidad": 3
    })
    assert r.status_code == 201, r.text
    assert r.json()["total"] == 150
    assert r.json()["estado"] == "completada"

    # Stock descontado.
    fila = db_session.execute(
        text("SELECT stock FROM productos WHERE id = :id"), {"id": pid}
    ).first()
    assert fila[0] == 7


def test_stock_insuficiente_400(client, db_session):
    vendedor = _usuario(db_session, "cmp2v@test.com", "vendedor")
    comprador = _usuario(db_session, "cmp2c@test.com")
    pid = _producto(db_session, vendedor, stock=2)

    r = client.post("/ordenes/comprar", json={
        "usuario_id": comprador, "producto_id": pid, "cantidad": 5
    })
    assert r.status_code == 400, r.text


def test_producto_oculto_no_comprable(client, db_session):
    vendedor = _usuario(db_session, "cmp3v@test.com", "vendedor")
    comprador = _usuario(db_session, "cmp3c@test.com")
    pid = _producto(db_session, vendedor, oculto=1)

    r = client.post("/ordenes/comprar", json={
        "usuario_id": comprador, "producto_id": pid, "cantidad": 1
    })
    assert r.status_code == 400, r.text


def test_compra_aparece_en_historial(client, db_session):
    vendedor = _usuario(db_session, "cmp4v@test.com", "vendedor")
    comprador = _usuario(db_session, "cmp4c@test.com")
    pid = _producto(db_session, vendedor, precio=20, stock=5)

    client.post("/ordenes/comprar", json={
        "usuario_id": comprador, "producto_id": pid, "cantidad": 1
    })

    hist = client.get(f"/ordenes/usuario/{comprador}")
    assert hist.status_code == 200
    assert len(hist.json()) == 1


def test_producto_inexistente_404(client, db_session):
    comprador = _usuario(db_session, "cmp5c@test.com")
    r = client.post("/ordenes/comprar", json={
        "usuario_id": comprador, "producto_id": 999999, "cantidad": 1
    })
    assert r.status_code == 404, r.text
