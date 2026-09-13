"""
Tests de PerfilVendedor: crear, validación automática, actualizar, restricción
a vendedor/influencer, visitante rechazado, duplicado rechazado.
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


def test_crear_perfil_vendedor_completo_se_valida(client, db_session):
    uid = _usuario(db_session, "pv1@test.com", "vendedor")

    resp = client.post("/perfil-vendedor/", json={
        "usuario_id": uid,
        "metodos_entrega": "Envío CDMX",
        "lugares_entrega": "Zona centro",
        "info_general": "Vendo ropa",
        "datos_bancarios": "CLABE 1234",
    })
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["validado"] is True
    assert data["metodos_entrega"] == "Envío CDMX"


def test_crear_perfil_incompleto_no_validado(client, db_session):
    uid = _usuario(db_session, "pv2@test.com", "vendedor")

    resp = client.post("/perfil-vendedor/", json={
        "usuario_id": uid,
        "metodos_entrega": "Envío",
        # faltan los demás campos
    })
    assert resp.status_code == 201, resp.text
    assert resp.json()["validado"] is False


def test_actualizar_completa_validacion(client, db_session):
    uid = _usuario(db_session, "pv3@test.com", "influencer")

    client.post("/perfil-vendedor/", json={"usuario_id": uid, "metodos_entrega": "X"})

    resp = client.put(f"/perfil-vendedor/usuario/{uid}", json={
        "lugares_entrega": "Todo MX",
        "info_general": "Influencer de moda",
        "datos_bancarios": "CLABE 999",
    })
    assert resp.status_code == 200, resp.text
    assert resp.json()["validado"] is True


def test_visitante_no_puede_crear_perfil_403(client, db_session):
    uid = _usuario(db_session, "pv4@test.com", "visitante")

    resp = client.post("/perfil-vendedor/", json={
        "usuario_id": uid,
        "metodos_entrega": "Envío",
        "lugares_entrega": "CDMX",
        "info_general": "Quiero vender",
        "datos_bancarios": "CLABE",
    })
    assert resp.status_code == 403, resp.text


def test_duplicado_409(client, db_session):
    uid = _usuario(db_session, "pv5@test.com", "vendedor")

    client.post("/perfil-vendedor/", json={"usuario_id": uid})
    r2 = client.post("/perfil-vendedor/", json={"usuario_id": uid})
    assert r2.status_code == 409


def test_check_validado(client, db_session):
    uid = _usuario(db_session, "pv6@test.com", "vendedor")

    # Sin perfil: no validado
    r = client.get(f"/perfil-vendedor/usuario/{uid}/validado")
    assert r.json()["validado"] is False

    # Crear completo
    client.post("/perfil-vendedor/", json={
        "usuario_id": uid,
        "metodos_entrega": "E", "lugares_entrega": "L",
        "info_general": "I", "datos_bancarios": "D",
    })
    r = client.get(f"/perfil-vendedor/usuario/{uid}/validado")
    assert r.json()["validado"] is True
