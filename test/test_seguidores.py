"""
Tests de Seguidores: seguir/dejar de seguir, auto-seguir al aceptar amistad,
contadores, no duplicados, no auto-seguirse.
"""
from sqlalchemy import text


def _usuario(db_session, email):
    r = db_session.execute(
        text("INSERT INTO usuarios (nombre, email, password, tipo_perfil, creado_en) "
             "VALUES ('U', :email, 'x', 'vendedor', NOW())"),
        {"email": email},
    )
    db_session.flush()
    return r.lastrowid


def test_seguir_y_contadores(client, db_session):
    a = _usuario(db_session, "seg1@test.com")
    b = _usuario(db_session, "seg1b@test.com")

    # a sigue a b
    r = client.post("/seguidores/", json={"seguidor_id": a, "seguido_id": b})
    assert r.status_code == 201, r.text

    # Contadores
    cnt = client.get(f"/seguidores/usuario/{b}/contadores").json()
    assert cnt["seguidores"] == 1
    assert cnt["siguiendo"] == 0

    cnt_a = client.get(f"/seguidores/usuario/{a}/contadores").json()
    assert cnt_a["siguiendo"] == 1

    # Check sigue
    ch = client.get(f"/seguidores/usuario/{a}/sigue/{b}").json()
    assert ch["sigue"] is True


def test_no_auto_seguir(client, db_session):
    a = _usuario(db_session, "seg2@test.com")
    r = client.post("/seguidores/", json={"seguidor_id": a, "seguido_id": a})
    assert r.status_code == 400


def test_no_duplicado_409(client, db_session):
    a = _usuario(db_session, "seg3@test.com")
    b = _usuario(db_session, "seg3b@test.com")

    r1 = client.post("/seguidores/", json={"seguidor_id": a, "seguido_id": b})
    assert r1.status_code == 201
    r2 = client.post("/seguidores/", json={"seguidor_id": a, "seguido_id": b})
    assert r2.status_code == 409


def test_dejar_de_seguir(client, db_session):
    a = _usuario(db_session, "seg4@test.com")
    b = _usuario(db_session, "seg4b@test.com")

    client.post("/seguidores/", json={"seguidor_id": a, "seguido_id": b})
    r = client.delete(f"/seguidores/?seguidor_id={a}&seguido_id={b}")
    assert r.status_code == 200

    ch = client.get(f"/seguidores/usuario/{a}/sigue/{b}").json()
    assert ch["sigue"] is False


def test_listas_siguiendo_y_seguidores(client, db_session):
    a = _usuario(db_session, "seg5@test.com")
    b = _usuario(db_session, "seg5b@test.com")
    c = _usuario(db_session, "seg5c@test.com")

    client.post("/seguidores/", json={"seguidor_id": a, "seguido_id": b})
    client.post("/seguidores/", json={"seguidor_id": a, "seguido_id": c})

    siguiendo = client.get(f"/seguidores/usuario/{a}/siguiendo").json()
    assert len(siguiendo) == 2

    seguidores_b = client.get(f"/seguidores/usuario/{b}/seguidores").json()
    assert any(u["id"] == a for u in seguidores_b)


def test_auto_seguir_al_aceptar_amistad(client, db_session):
    a = _usuario(db_session, "seg6@test.com")
    b = _usuario(db_session, "seg6b@test.com")

    # Crear amistad pendiente
    r = client.post("/amistades/", json={"usuario_id": a, "amigo_id": b, "estado": "pendiente"})
    assert r.status_code == 201
    amistad_id = r.json()["id"]

    # Aceptar
    r = client.patch(f"/amistades/{amistad_id}/estado", json={"estado": "aceptada"})
    assert r.status_code == 200

    # Ambos se siguen mutuamente
    assert client.get(f"/seguidores/usuario/{a}/sigue/{b}").json()["sigue"] is True
    assert client.get(f"/seguidores/usuario/{b}/sigue/{a}").json()["sigue"] is True
