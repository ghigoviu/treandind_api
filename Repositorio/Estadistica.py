from sqlalchemy import func
from sqlalchemy.orm import Session

from Modelo.Orden import Orden
from Modelo.OrdenDetalle import OrdenDetalle
from Modelo.Producto import Producto
from Modelo.Usuario import Usuario


class EstadisticaRepo:
    """Agregaciones de ventas para el dashboard del vendedor.

    Todas las métricas se calculan sobre las órdenes 'completadas' que incluyen
    productos del vendedor indicado.
    """

    @staticmethod
    def _base_query(db: Session, vendedor_id: int):
        """Query base: detalles de venta de productos del vendedor en órdenes completadas."""
        return (
            db.query(OrdenDetalle, Orden, Producto)
            .join(Orden, OrdenDetalle.orden_id == Orden.id)
            .join(Producto, OrdenDetalle.producto_id == Producto.id)
            .filter(
                Producto.usuario_id == vendedor_id,
                Orden.estado == 'completada',
            )
        )

    @staticmethod
    def resumen(db: Session, vendedor_id: int) -> dict:
        """Devuelve un dict con hasta 6 métricas/filtros de ventas."""
        filas = EstadisticaRepo._base_query(db, vendedor_id).all()

        total_ventas = 0
        total_ingresos = 0.0
        unidades = 0
        por_producto = {}
        por_comprador = {}
        por_mes = {}

        for detalle, orden, producto in filas:
            subtotal = detalle.cantidad * detalle.precio_unit
            total_ventas += 1
            total_ingresos += subtotal
            unidades += detalle.cantidad

            # 1) Ventas por producto (top productos).
            por_producto.setdefault(producto.nombre, {"unidades": 0, "ingresos": 0.0})
            por_producto[producto.nombre]["unidades"] += detalle.cantidad
            por_producto[producto.nombre]["ingresos"] += subtotal

            # 2) Compradores con más compras.
            por_comprador.setdefault(orden.usuario_id, {"compras": 0, "gastado": 0.0})
            por_comprador[orden.usuario_id]["compras"] += 1
            por_comprador[orden.usuario_id]["gastado"] += subtotal

            # 3) Ventas por mes (YYYY-MM).
            if orden.creado_en:
                clave_mes = orden.creado_en.strftime("%Y-%m")
                por_mes.setdefault(clave_mes, {"ventas": 0, "ingresos": 0.0})
                por_mes[clave_mes]["ventas"] += 1
                por_mes[clave_mes]["ingresos"] += subtotal

        # Top productos por unidades.
        top_productos = sorted(
            [{"nombre": n, **v} for n, v in por_producto.items()],
            key=lambda x: x["unidades"], reverse=True
        )[:5]

        # Top compradores: enriquecer con nombre.
        top_compradores = []
        compradores_ordenados = sorted(
            por_comprador.items(), key=lambda kv: kv[1]["compras"], reverse=True
        )[:5]
        for uid, datos in compradores_ordenados:
            u = db.query(Usuario).filter(Usuario.id == uid).first()
            top_compradores.append({
                "usuario_id": uid,
                "nombre": u.nombre if u else "Usuario",
                "compras": datos["compras"],
                "gastado": round(datos["gastado"], 2),
            })

        ventas_por_mes = sorted(
            [{"mes": m, **v} for m, v in por_mes.items()],
            key=lambda x: x["mes"]
        )

        return {
            "total_ventas": total_ventas,            # 4) número total de ventas
            "total_ingresos": round(total_ingresos, 2),  # 5) ingresos totales
            "unidades_vendidas": unidades,           # 6) unidades vendidas
            "top_productos": top_productos,
            "top_compradores": top_compradores,
            "ventas_por_mes": ventas_por_mes,
        }
