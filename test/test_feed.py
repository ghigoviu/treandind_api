"""
Tests del feed/timeline: solo productos de vendedores seguidos, excluye ocultos,
vacío si no sigue a nadie, orden por fecha.
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


def test_feed_solo_de_seguidos(client, db_session):
    visitante = _usuario(db_session, "fd1@test.com", "visitante")
    vendedor_seguido = _usuario(db_session, "fd1s@test.com")
    vendedor_no_seguido = _usuario(db_session, "fd1n@test.com")

    _producto(db_session, vendedor_seguido, "DeSeguido")
    _producto(db_session, vendedor_no_seguido, "DeOtro")

    # Seguir solo a uno.
    client.post("/seguidores/", json={"seguidor_id": visitante, "seguido_id": vendedor_seguido})

    feed = client.get(f"/productos/feed/{visitante}").json()
    nombres = [p["nombre"] for p in feed]
    assert "DeSeguido" in nombres
    assert "DeOtro" not in nombres


def test_feed_excluye_ocultos(client, db_session):
    visitante = _usuario(db_session, "fd2@test.com", "visitante")
    vendedor = _usuario(db_session, "fd2v@test.com")

    _producto(db_session, vendedor, "Visible", oculto=0)
    _producto(db_session, vendedor, "Oculto", oculto=1)

    client.post("/seguidores/", json={"seguidor_id": visitante, "seguido_id": vendedor})

    feed = client.get(f"/productos/feed/{visitante}").json()
    nombres = [p["nombre"] for p in feed]
    assert "Visible" in nombres
    assert "Oculto" not in nombres


def test_feed_vacio_sin_seguidos(client, db_session):
    visitante = _usuario(db_session, "fd3@test.com", "visitante")
    vendedor = _usuario(db_session, "fd3v@test.com")
    _producto(db_session, vendedor, "Algo")

    # No sigue a nadie.
    feed = client.get(f"/productos/feed/{visitante}").json()
    assert feed == []
