from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Modelo.Orden import Orden
from Modelo.OrdenDetalle import OrdenDetalle
from Schema.Orden import OrdenCreate
from typing import Optional, List
from fastapi import HTTPException


class OrdenRepo:
    @staticmethod
    def fetch_by_id(db: Session, orden_id: int) -> Optional[Orden]:
        return db.query(Orden).filter(Orden.id == orden_id).first()

    @staticmethod
    def fetch_all(db: Session) -> List[Orden]:
        return db.query(Orden).all()

    @staticmethod
    def fetch_by_usuario(db: Session, usuario_id: int) -> List[Orden]:
        """Compras realizadas por un usuario (historial de compras)."""
        return (
            db.query(Orden)
            .filter(Orden.usuario_id == usuario_id)
            .order_by(Orden.creado_en.desc())
            .all()
        )

    @staticmethod
    def fetch_ventas_por_vendedor(db: Session, vendedor_id: int) -> List[dict]:
        """Ventas de los productos publicados por un vendedor.

        Devuelve una lista de dicts con datos de la venta (orden + detalle +
        producto), útil para el historial de ventas del vendedor.
        """
        from Modelo.Producto import Producto

        filas = (
            db.query(OrdenDetalle, Orden, Producto)
            .join(Orden, OrdenDetalle.orden_id == Orden.id)
            .join(Producto, OrdenDetalle.producto_id == Producto.id)
            .filter(Producto.usuario_id == vendedor_id)
            .order_by(Orden.creado_en.desc())
            .all()
        )

        resultado = []
        for detalle, orden, producto in filas:
            resultado.append({
                "orden_id": orden.id,
                "estado": orden.estado,
                "creado_en": orden.creado_en,
                "comprador_id": orden.usuario_id,
                "producto_id": producto.id,
                "producto_nombre": producto.nombre,
                "cantidad": detalle.cantidad,
                "precio_unit": detalle.precio_unit,
                "subtotal": detalle.cantidad * detalle.precio_unit,
            })
        return resultado

    @staticmethod
    def fetch_detalles(db: Session, orden_id: int) -> List[OrdenDetalle]:
        return db.query(OrdenDetalle).filter(OrdenDetalle.orden_id == orden_id).all()

    @staticmethod
    def create(db: Session, orden_data: OrdenCreate) -> Orden:
        try:
            orden_dict = orden_data.orden.dict()
            detalles = orden_data.detalles

            orden = Orden(**orden_dict)
            db.add(orden)
            db.flush()  # Para obtener orden.id antes de insertar detalles

            for detalle_data in detalles:
                # El schema usa 'precio_unitario' pero el modelo usa 'precio_unit'.
                detalle = OrdenDetalle(
                    orden_id=orden.id,
                    cantidad=detalle_data.cantidad,
                    precio_unit=detalle_data.precio_unitario,
                    producto_id=detalle_data.producto_id,
                    evento_id=detalle_data.evento_id,
                )
                db.add(detalle)

            db.commit()
            db.refresh(orden)
            return orden

        except IntegrityError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error al crear la orden: " + str(e))

    @staticmethod
    def comprar(db: Session, usuario_id: int, producto_id: int, cantidad: int) -> Orden:
        """Compra un producto: valida y descuenta stock, crea orden + detalle,
        todo de forma atómica (un solo commit)."""
        from Modelo.Producto import Producto
        from Modelo.Usuario import Usuario

        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")

        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado.")

        if producto.oculto:
            raise HTTPException(status_code=400, detail="Este producto no está disponible.")

        if producto.stock < cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente. Disponibles: {producto.stock}."
            )

        total = round(producto.precio * cantidad, 2)

        orden = Orden(usuario_id=usuario_id, estado='completada', total=total)
        db.add(orden)
        db.flush()

        detalle = OrdenDetalle(
            orden_id=orden.id,
            cantidad=cantidad,
            precio_unit=producto.precio,
            producto_id=producto_id,
        )
        db.add(detalle)

        # Descontar stock de forma atómica.
        producto.stock -= cantidad

        # Notificar al vendedor de la nueva venta.
        vendedor = None
        if producto.usuario_id:
            from Repositorio.Notificacion import NotificacionRepo
            NotificacionRepo.crear(
                db, producto.usuario_id, "venta",
                f"¡Vendiste {cantidad} x '{producto.nombre}'!", ref_id=orden.id
            )
            vendedor = db.query(Usuario).filter(Usuario.id == producto.usuario_id).first()

        # Capturar datos para el email antes del commit.
        datos_email = {
            "vendedor_email": vendedor.email if vendedor else None,
            "comprador_email": usuario.email,
            "producto_nombre": producto.nombre,
            "cantidad": cantidad,
            "total": total,
        }

        db.commit()
        db.refresh(orden)

        # Enviar los 3 correos de la venta DESPUÉS del commit (no rompe la compra
        # si el email falla; el servicio ya captura sus propios errores).
        from Servicios.Email import enviar_correos_venta
        enviar_correos_venta(
            datos_email["vendedor_email"],
            datos_email["comprador_email"],
            datos_email["producto_nombre"],
            datos_email["cantidad"],
            datos_email["total"],
        )

        return orden

    @staticmethod
    def delete(db: Session, orden_id: int) -> Optional[Orden]:
        orden = db.query(Orden).filter(Orden.id == orden_id).first()
        if orden:
            db.delete(orden)
            db.commit()
            return orden
        return None
