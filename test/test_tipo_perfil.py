"""
Tests de tipo_perfil en Usuario: registro con cada tipo, default visitante,
tipo inválido rechazado (422), y que el __init__ corregido acepta todos los campos.
"""


def test_registro_default_visitante(client):
    resp = client.post("/usuarios/", json={
        "nombre": "Visitante", "email": "vis@test.com", "password": "x"
    })
    assert resp.status_code == 201, resp.text
    assert resp.json()["tipo_perfil"] == "visitante"


def test_registro_como_vendedor(client):
    resp = client.post("/usuarios/", json={
        "nombre": "Vendedor", "email": "vend@test.com", "password": "x",
        "tipo_perfil": "vendedor"
    })
    assert resp.status_code == 201, resp.text
    assert resp.json()["tipo_perfil"] == "vendedor"


def test_registro_como_influencer(client):
    resp = client.post("/usuarios/", json={
        "nombre": "Influencer", "email": "inf@test.com", "password": "x",
        "tipo_perfil": "influencer"
    })
    assert resp.status_code == 201, resp.text
    assert resp.json()["tipo_perfil"] == "influencer"


def test_tipo_perfil_invalido_422(client):
    resp = client.post("/usuarios/", json={
        "nombre": "Raro", "email": "raro@test.com", "password": "x",
        "tipo_perfil": "admin"
    })
    assert resp.status_code == 422, resp.text


def test_init_acepta_todos_los_campos(client):
    """El __init__ de Usuario ahora acepta bio, phone, birthdate, etc. sin TypeError."""
    resp = client.post("/usuarios/", json={
        "nombre": "Completo", "email": "full@test.com", "password": "x",
        "tipo_perfil": "vendedor",
        "bio": "Soy vendedor",
        "phone": "+52123456",
        "imagen_perfil": "http://img/perfil.jpg",
        "imagen_portada": "http://img/portada.jpg",
    })
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["bio"] == "Soy vendedor"
    assert data["phone"] == "+52123456"
    assert data["imagen_perfil"] == "http://img/perfil.jpg"


def test_obtener_usuario_devuelve_tipo_perfil(client):
    r = client.post("/usuarios/", json={
        "nombre": "ObtTest", "email": "obt@test.com", "password": "x",
        "tipo_perfil": "vendedor"
    })
    uid = r.json()["id"]
    det = client.get(f"/usuarios/id/{uid}")
    assert det.status_code == 200
    assert det.json()["tipo_perfil"] == "vendedor"
