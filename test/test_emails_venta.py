"""
Tests de emails de venta: al comprar se envían 3 correos (vendedor, comprador,
admin); la compra no falla si el email falla; el servicio de email standalone.
"""
from sqlalchemy import text

from Servicios import Email


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


def test_compra_envia_tres_correos(client, db_session):
    Email._reset_buzon()

    vendedor = _usuario(db_session, "em1v@test.com")
    comprador = _usuario(db_session, "em1c@test.com", "visitante")
    pid = _producto(db_session, vendedor)

    r = client.post("/ordenes/comprar", json={
        "usuario_id": comprador, "producto_id": pid, "cantidad": 1
    })
    assert r.status_code == 201, r.text

    # Se registraron 3 correos (email desactivado -> buzón en memoria).
    destinatarios = [m["para"] for m in Email._buzon_pruebas]
    assert "em1v@test.com" in destinatarios  # vendedor
    assert "em1c@test.com" in destinatarios  # comprador
    assert len(Email._buzon_pruebas) == 3    # + admin


def test_enviar_correos_venta_devuelve_conteo(db_session):
    Email._reset_buzon()
    enviados = Email.enviar_correos_venta(
        "v@test.com", "c@test.com", "Producto X", 2, 200.0
    )
    assert enviados == 3


def test_enviar_email_destinatario_vacio(db_session):
    assert Email.enviar_email("", "asunto", "cuerpo") is False
