"""
Tests de notificaciones: se generan en amistad, seguidor, venta y nuevo
producto; listar, contador no leídas, marcar leída/todas.
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


def _producto(db_session, vendedor_id, precio=100, stock=10):
    r = db_session.execute(
        text("INSERT INTO productos (nombre, slug, precio, stock, tipo, oculto, img_portada, "
             "creado_en, requiere_edad, calificacion, usuario_id) "
             "VALUES ('P', 'p', :precio, :stock, 'fisico', 0, '', NOW(), 0, 0, :uid)"),
        {"precio": precio, "stock": stock, "uid": vendedor_id},
    )
    db_session.flush()
    return r.lastrowid


def _validar_vendedor(client, uid):
    client.post("/perfil-vendedor/", json={
        "usuario_id": uid, "metodos_entrega": "E", "lugares_entrega": "L",
        "info_general": "I", "datos_bancarios": "D",
    })


def test_notificacion_de_amistad(client, db_session):
    a = _usuario(db_session, "n1a@test.com")
    b = _usuario(db_session, "n1b@test.com")

    client.post("/amistades/", json={"usuario_id": a, "amigo_id": b, "estado": "pendiente"})

    notifs = client.get(f"/notificaciones/usuario/{b}").json()
    assert any(n["tipo"] == "amistad" for n in notifs)


def test_notificacion_de_seguidor(client, db_session):
    a = _usuario(db_session, "n2a@test.com")
    b = _usuario(db_session, "n2b@test.com")

    client.post("/seguidores/", json={"seguidor_id": a, "seguido_id": b})

    notifs = client.get(f"/notificaciones/usuario/{b}").json()
    assert any(n["tipo"] == "seguidor" for n in notifs)


def test_notificacion_de_venta(client, db_session):
    vendedor = _usuario(db_session, "n3v@test.com")
    comprador = _usuario(db_session, "n3c@test.com", "visitante")
    pid = _producto(db_session, vendedor)

    client.post("/ordenes/comprar", json={
        "usuario_id": comprador, "producto_id": pid, "cantidad": 1
    })

    notifs = client.get(f"/notificaciones/usuario/{vendedor}").json()
    assert any(n["tipo"] == "venta" for n in notifs)


def test_notificacion_nuevo_producto_a_seguidores(client, db_session):
    vendedor = _usuario(db_session, "n4v@test.com")
    seguidor = _usuario(db_session, "n4s@test.com", "visitante")
    _validar_vendedor(client, vendedor)

    # El seguidor sigue al vendedor.
    client.post("/seguidores/", json={"seguidor_id": seguidor, "seguido_id": vendedor})

    # El vendedor publica un producto.
    client.post("/productos/", json={
        "nombre": "Novedad", "precio": 50, "usuario_id": vendedor,
    })

    notifs = client.get(f"/notificaciones/usuario/{seguidor}").json()
    assert any(n["tipo"] == "nuevo_producto" for n in notifs)


def test_contador_y_marcar_leidas(client, db_session):
    a = _usuario(db_session, "n5a@test.com")
    b = _usuario(db_session, "n5b@test.com")

    # Generar 1 notificación (seguidor) para b.
    client.post("/seguidores/", json={"seguidor_id": a, "seguido_id": b})

    cont = client.get(f"/notificaciones/usuario/{b}/contador").json()
    assert cont["no_leidas"] >= 1

    # Marcar todas leídas.
    client.patch(f"/notificaciones/usuario/{b}/leer-todas")
    cont2 = client.get(f"/notificaciones/usuario/{b}/contador").json()
    assert cont2["no_leidas"] == 0
