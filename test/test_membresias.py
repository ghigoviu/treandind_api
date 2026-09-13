"""
Tests de membresías/VIP: crear paquete (solo vendedor), suscribirse, producto
VIP solo visible para suscriptores activos, vencimiento genera alerta.
"""
from datetime import datetime, timedelta
from sqlalchemy import text


def _usuario(db_session, email, tipo='vendedor'):
    r = db_session.execute(
        text("INSERT INTO usuarios (nombre, email, password, tipo_perfil, creado_en) "
             "VALUES ('U', :email, 'x', :tipo, NOW())"),
        {"email": email, "tipo": tipo},
    )
    db_session.flush()
    return r.lastrowid


def _producto_vip(db_session, vendedor_id, nombre="VIP"):
    r = db_session.execute(
        text("INSERT INTO productos (nombre, slug, precio, stock, tipo, oculto, vip, "
             "img_portada, creado_en, requiere_edad, calificacion, usuario_id) "
             "VALUES (:n, 'p', 100, 5, 'fisico', 0, 1, '', NOW(), 0, 0, :uid)"),
        {"n": nombre, "uid": vendedor_id},
    )
    db_session.flush()
    return r.lastrowid


def test_crear_paquete_solo_vendedor(client, db_session):
    vendedor = _usuario(db_session, "mem1v@test.com", "vendedor")
    r = client.post("/membresias/paquetes", json={
        "vendedor_id": vendedor, "titulo": "Plan Oro", "frecuencia": "mensual",
        "costo": 99.0, "descripcion": "Acceso VIP",
    })
    assert r.status_code == 201, r.text
    assert r.json()["titulo"] == "Plan Oro"


def test_visitante_no_crea_paquete_403(client, db_session):
    visitante = _usuario(db_session, "mem2@test.com", "visitante")
    r = client.post("/membresias/paquetes", json={
        "vendedor_id": visitante, "titulo": "X", "frecuencia": "mensual", "costo": 10.0,
    })
    assert r.status_code == 403, r.text


def test_frecuencia_invalida_422(client, db_session):
    vendedor = _usuario(db_session, "mem3v@test.com", "vendedor")
    r = client.post("/membresias/paquetes", json={
        "vendedor_id": vendedor, "titulo": "X", "frecuencia": "diaria", "costo": 10.0,
    })
    assert r.status_code == 422, r.text


def test_vip_solo_para_suscriptores(client, db_session):
    vendedor = _usuario(db_session, "mem4v@test.com", "vendedor")
    suscriptor = _usuario(db_session, "mem4s@test.com", "visitante")
    extrano = _usuario(db_session, "mem4x@test.com", "visitante")
    _producto_vip(db_session, vendedor, "ProductoVIP")

    # Crear paquete y suscribir al suscriptor.
    pkg = client.post("/membresias/paquetes", json={
        "vendedor_id": vendedor, "titulo": "Plan", "frecuencia": "mensual", "costo": 50.0,
    }).json()
    client.post("/membresias/suscribir", json={"usuario_id": suscriptor, "paquete_id": pkg["id"]})

    # El suscriptor ve el producto VIP.
    r_sus = client.get(f"/membresias/vip/vendedor/{vendedor}/solicitante/{suscriptor}")
    assert len(r_sus.json()) == 1

    # El extraño NO ve el producto VIP.
    r_ext = client.get(f"/membresias/vip/vendedor/{vendedor}/solicitante/{extrano}")
    assert r_ext.json() == []

    # El producto VIP no aparece en el catálogo público.
    publicos = client.get("/productos/").json()
    assert not any(p["nombre"] == "ProductoVIP" for p in publicos)


def test_vencimiento_genera_alerta(client, db_session):
    vendedor = _usuario(db_session, "mem5v@test.com", "vendedor")
    suscriptor = _usuario(db_session, "mem5s@test.com", "visitante")

    pkg = client.post("/membresias/paquetes", json={
        "vendedor_id": vendedor, "titulo": "Plan", "frecuencia": "mensual", "costo": 50.0,
    }).json()

    # Insertar una suscripción ya vencida directamente.
    vencida = datetime.now() - timedelta(days=1)
    db_session.execute(
        text("INSERT INTO suscripciones_membresia (usuario_id, paquete_id, vendedor_id, "
             "estado, inicio, vencimiento, creado_en) "
             "VALUES (:u, :p, :v, 'activa', NOW(), :venc, NOW())"),
        {"u": suscriptor, "p": pkg["id"], "v": vendedor, "venc": vencida},
    )
    db_session.flush()

    res = client.post("/membresias/procesar-vencimientos")
    assert res.status_code == 200
    assert res.json()["vencidas"] >= 1

    # El suscriptor recibió notificación de membresía.
    notifs = client.get(f"/notificaciones/usuario/{suscriptor}").json()
    assert any(n["tipo"] == "membresia" for n in notifs)
