"""
Tests de gestión de productos del vendedor: editar, ocultar (excluido de
listados públicos pero visible al dueño), eliminar.
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


def test_editar_producto(client, db_session):
    v = _usuario(db_session, "gp1@test.com")
    pid = _producto(db_session, v, "Original")

    r = client.put(f"/productos/{pid}", json={"nombre": "Editado", "precio": 250})
    assert r.status_code == 200, r.text
    assert r.json()["nombre"] == "Editado"
    assert r.json()["precio"] == 250


def test_ocultar_excluye_de_listado_publico(client, db_session):
    v = _usuario(db_session, "gp2@test.com")
    pid = _producto(db_session, v, "ParaOcultar")

    # Aparece en listado público inicialmente.
    publicos = client.get("/productos/").json()
    assert any(p["id"] == pid for p in publicos)

    # Ocultar via PUT.
    r = client.put(f"/productos/{pid}", json={"oculto": True})
    assert r.status_code == 200, r.text
    assert r.json()["oculto"] is True

    # Ya no aparece en listado público.
    publicos = client.get("/productos/").json()
    assert not any(p["id"] == pid for p in publicos)

    # Pero sí aparece en el listado del dueño.
    del_vendedor = client.get(f"/productos/vendedor/{v}").json()
    assert any(p["id"] == pid for p in del_vendedor)


def test_mostrar_de_nuevo(client, db_session):
    v = _usuario(db_session, "gp3@test.com")
    pid = _producto(db_session, v, "Toggle", oculto=1)

    # Está oculto -> no en público.
    assert not any(p["id"] == pid for p in client.get("/productos/").json())

    # Mostrar de nuevo.
    client.put(f"/productos/{pid}", json={"oculto": False})
    assert any(p["id"] == pid for p in client.get("/productos/").json())


def test_eliminar_producto(client, db_session):
    v = _usuario(db_session, "gp4@test.com")
    pid = _producto(db_session, v, "Borrar")

    r = client.delete(f"/productos/{pid}")
    assert r.status_code == 200, r.text

    # Ya no existe.
    assert client.get(f"/productos/id/{pid}").status_code == 404
