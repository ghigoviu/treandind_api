"""
Servicio de envío de correos electrónicos (SMTP).

Diseñado para no romper el flujo de negocio si el envío falla: cualquier error
se registra y se ignora. En desarrollo/tests el envío puede desactivarse con
`email.enabled = false` (o EMAIL_ENABLED=0), en cuyo caso los correos solo se
registran en una lista en memoria (para poder verificarlos en tests).
"""
import smtplib
import logging
from email.mime.text import MIMEText

from Datos.Config import get_email_config

logger = logging.getLogger("treanding.email")

# Buzón en memoria para inspección en tests cuando el envío está desactivado.
_buzon_pruebas = []


def _reset_buzon():
    _buzon_pruebas.clear()


def enviar_email(destinatario: str, asunto: str, cuerpo: str) -> bool:
    """Envía un correo. Devuelve True si se envió (o se registró en modo test),
    False si hubo un error. Nunca lanza excepción hacia el llamador."""
    cfg = get_email_config()

    if not destinatario:
        return False

    # Modo desactivado: solo registrar (dev/tests).
    if not cfg["enabled"]:
        _buzon_pruebas.append({
            "para": destinatario, "asunto": asunto, "cuerpo": cuerpo
        })
        logger.info("Email (simulado) a %s: %s", destinatario, asunto)
        return True

    try:
        msg = MIMEText(cuerpo, "plain", "utf-8")
        msg["Subject"] = asunto
        msg["From"] = cfg["from"]
        msg["To"] = destinatario

        with smtplib.SMTP(cfg["host"], cfg["port"], timeout=10) as server:
            if cfg["user"]:
                server.starttls()
                server.login(cfg["user"], cfg["password"])
            server.sendmail(cfg["from"], [destinatario], msg.as_string())
        return True
    except Exception as e:
        # No romper el flujo de negocio si el email falla.
        logger.warning("Fallo al enviar email a %s: %s", destinatario, e)
        return False


def enviar_correos_venta(vendedor_email, comprador_email, producto_nombre,
                         cantidad, total, formas_entrega=""):
    """Envía los 3 correos de una venta: vendedor, comprador y administrador.
    Devuelve el número de correos enviados con éxito."""
    cfg = get_email_config()
    admin_email = cfg["admin"]

    resumen = (
        f"Producto: {producto_nombre}\n"
        f"Cantidad: {cantidad}\n"
        f"Total: ${total}\n"
        f"Formas de entrega: {formas_entrega or 'Por coordinar con el vendedor'}\n"
    )

    enviados = 0
    if enviar_email(vendedor_email, "¡Tienes una nueva venta en Treanding!",
                    f"Has vendido un producto.\n\n{resumen}"):
        enviados += 1
    if enviar_email(comprador_email, "Confirmación de tu compra en Treanding",
                    f"Gracias por tu compra.\n\n{resumen}"):
        enviados += 1
    if enviar_email(admin_email, "Nueva venta registrada en Treanding",
                    f"Se registró una venta en la plataforma.\n\n{resumen}"):
        enviados += 1

    return enviados
