from sqlalchemy.orm import Session, joinedload
from Modelo.Producto import Producto
from typing import List, Optional

from Modelo.ProductoAtributo import ProductoAtributo
from Modelo.ProductoImagen import ProductoImagen
from Schema.Producto import ProductoCreate


class ProductoRepo:
    @staticmethod
    def fetch_by_id(db: Session, producto_id: int) -> Optional[Producto]:
        return db.query(Producto).filter(Producto.id == producto_id).first()

    def fetch_by_id_personalizado(db: Session, producto_id: int) -> Optional[dict]:
        producto = (
            db.query(Producto)
            .filter(Producto.id == producto_id)
            .options(
                joinedload(Producto.categoria),
                joinedload(Producto.usuario_creador),
                joinedload(Producto.atributos),
                joinedload(Producto.imagenes),
                joinedload(Producto.reviews)
            )
            .first()
        )

        if not producto:
            return None

        # Agrupamos los atributos
        atributos_agrupados = {}
        for attr in producto.atributos:
            if attr.nombre not in atributos_agrupados:
                atributos_agrupados[attr.nombre] = []
            atributos_agrupados[attr.nombre].append({
                "id": attr.id,
                "valor": attr.valor,
                "precio": attr.precio,
                "cantidad": attr.cantidad
            })

        atributos_formateados = [
            {"nombre": nombre, "valores": valores}
            for nombre, valores in atributos_agrupados.items()
        ]

        # Creamos la respuesta personalizada como dict
        return {
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "stock": producto.stock,
            "tipo": producto.tipo,
            "oculto": producto.oculto,
            "requiere_edad": producto.requiere_edad,
            "descripcion": producto.descripcion,
            "img_portada": producto.img_portada,
            "calificacion": producto.calificacion,
            "creado_en": producto.creado_en,
            "categoria": {
                "id": producto.categoria.id,
                "nombre": producto.categoria.nombre,
            } if producto.categoria else None,
            "usuario_creador": {
                "id": producto.usuario_creador.id,
                "nombre": producto.usuario_creador.nombre,
                "email": producto.usuario_creador.email
            } if producto.usuario_creador else None,
            "imagenes": [
                {
                    "id": img.id,
                    "url": img.url,
                }
                for img in producto.imagenes
            ],
            "reviews": [
                {
                    "id": review.id,
                    "comentario": review.comentario,
                    "calificacion": review.calificacion,
                    "usuario_id": review.usuario_id,
                    "usuario": {
                        "id": review.usuario.id,
                        "nombre": review.usuario.nombre,
                        "imagen_perfil": review.usuario.imagen_perfil,
                    } if review.usuario else None
                }
                for review in producto.reviews
            ],
            "atributos": atributos_formateados
        }

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 100) -> List[Producto]:
        # Los listados públicos excluyen productos ocultos y VIP.
        return (
            db.query(Producto)
            .filter(Producto.oculto == False, Producto.vip == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, producto_data: ProductoCreate) -> Producto:
        from fastapi import HTTPException, status
        from Repositorio.PerfilVendedor import PerfilVendedorRepo
        from Modelo.Usuario import Usuario

        # Validar que el creador sea vendedor/influencer validado.
        usuario = db.query(Usuario).filter(Usuario.id == producto_data.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        if usuario.tipo_perfil not in ('vendedor', 'influencer'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo vendedores o influencers pueden publicar productos."
            )
        if not PerfilVendedorRepo.esta_validado(db, producto_data.usuario_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Debes validar tu perfil de vendedor antes de publicar."
            )

        producto = Producto(
            nombre=producto_data.nombre,
            descripcion=producto_data.descripcion,
            precio=producto_data.precio,
            stock=producto_data.stock,
            tipo=producto_data.tipo,
            vip=producto_data.vip,
            usuario_id=producto_data.usuario_id,
            categoria_id=producto_data.categoria_id,
            colaboracion_id=producto_data.colaboracion_id,
            requiere_edad=producto_data.requiere_edad,
            imagen_portada=producto_data.img_portada,
        )
        db.add(producto)
        db.flush()  # Para obtener el ID antes del commit

        # Crear atributos relacionados (los 3 tabs)
        for attr in producto_data.atributos:
            atributo = ProductoAtributo(
                producto_id=producto.id,
                nombre=attr.nombre,
                valor=attr.valor
            )
            db.add(atributo)

        # Crear imágenes relacionadas
        for img in producto_data.imagenes:
            imagen = ProductoImagen(
                producto_id=producto.id,
                url=img.url,
                es_portada=img.es_portada
            )
            db.add(imagen)

        # Notificar a los seguidores del vendedor sobre el nuevo producto.
        from Repositorio.Notificacion import NotificacionRepo
        from Modelo.Seguidor import Seguidor
        seguidores_ids = [
            r[0] for r in
            db.query(Seguidor.seguidor_id).filter(Seguidor.seguido_id == producto_data.usuario_id).all()
        ]
        for seg_id in seguidores_ids:
            NotificacionRepo.crear(
                db, seg_id, "nuevo_producto",
                f"{usuario.nombre} publicó un nuevo producto: '{producto.nombre}'.",
                ref_id=producto.id
            )

        db.commit()
        db.refresh(producto)
        return producto

    @staticmethod
    def update(db: Session, producto_id: int, producto_data: dict) -> Optional[Producto]:
        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if producto:
            for key, value in producto_data.items():
                if value is not None:
                    setattr(producto, key, value)
            db.commit()
            db.refresh(producto)
            return producto
        return None

    @staticmethod
    def fetch_by_vendedor(db: Session, usuario_id: int, incluir_ocultos: bool = True) -> List[Producto]:
        q = db.query(Producto).filter(Producto.usuario_id == usuario_id)
        if not incluir_ocultos:
            q = q.filter(Producto.oculto == False)
        return q.all()

    @staticmethod
    def fetch_vip_por_vendedor(db: Session, vendedor_id: int, solicitante_id: int) -> List[Producto]:
        """Productos VIP de un vendedor, visibles solo si el solicitante tiene
        una suscripción activa con ese vendedor (o es el propio vendedor)."""
        from Repositorio.Membresia import MembresiaRepo

        es_dueno = solicitante_id == vendedor_id
        if not es_dueno and not MembresiaRepo.suscripcion_activa(db, solicitante_id, vendedor_id):
            return []
        return (
            db.query(Producto)
            .filter(
                Producto.usuario_id == vendedor_id,
                Producto.vip == True,
                Producto.oculto == False,
            )
            .all()
        )

    @staticmethod
    def fetch_feed(db: Session, usuario_id: int, skip: int = 0, limit: int = 50) -> List[Producto]:
        """Productos (no ocultos) de los vendedores que el usuario sigue,
        ordenados por fecha de creación descendente (timeline)."""
        from Modelo.Seguidor import Seguidor

        seguidos_ids = [
            r[0] for r in
            db.query(Seguidor.seguido_id).filter(Seguidor.seguidor_id == usuario_id).all()
        ]
        if not seguidos_ids:
            return []
        return (
            db.query(Producto)
            .filter(
                Producto.usuario_id.in_(seguidos_ids),
                Producto.oculto == False,
                Producto.vip == False,
            )
            .order_by(Producto.creado_en.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def delete(db: Session, producto_id: int) -> Optional[int]:
        """Elimina un producto y sus dependencias (atributos, imágenes, reviews).
        Devuelve el id eliminado (capturado antes del commit para evitar objeto
        detached) o None si no existía."""
        from Modelo.ProductoImagen import ProductoImagen
        from Modelo.Review import Review

        producto = db.query(Producto).filter(Producto.id == producto_id).first()
        if not producto:
            return None

        pid = producto.id
        # Borrar dependencias primero para no violar FKs.
        db.query(ProductoAtributo).filter(ProductoAtributo.producto_id == pid).delete()
        db.query(ProductoImagen).filter(ProductoImagen.producto_id == pid).delete()
        db.query(Review).filter(Review.producto_id == pid).delete()

        db.delete(producto)
        db.commit()
        return pid
