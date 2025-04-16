# 🐍 Trending API - Gestión de Usuarios, Productos y Eventos

Este proyecto es una API RESTful construida con [FastAPI](https://fastapi.tiangolo.com/) que implementa un enfoque 
limpio y modular basado en clases para controladores, usando SQLAlchemy para la ORM y Pydantic para validaciones.

---
## 🧑‍💻 Autor

Desarrollado por [@ghigoviu](https://github.com/ghigoviu)`

---

## 🚀 Características principales

- ✅ FastAPI para un rendimiento y documentación automáticos
- ✅ SQLAlchemy para la gestión de modelos y base de datos
- ✅ Pydantic para validación de datos
- ✅ Controladores organizados con clases y decoradores
- ✅ Estructura escalable por módulos
- ✅ CRUD completo para Usuarios (y extensible a otros recursos)
- ✅ Separación clara entre capas: Controlador, Servicio, Repositorio, Modelos

---
## 🧩 Extensiones posibles

- Autenticación con JWT / OAuth2
- Soporte para roles y permisos
- Upload de imágenes
- Relación entre entidades (productos, eventos, etc.)
- Tests automatizados (con pytest)
- Dockerización del proyecto

---
## Endpoints

### Endpoints de Producto:

-   POST /productos/
    
    - Descripción: Crea un nuevo producto con atributos e imágenes asociadas.
    - Requiere: ProductoCreate (incluye nombre, descripción, precio, stock, etc.)
    - Responde: ProductoRead (producto creado)

-   GET /productos/

    - Descripción: Obtiene todos los productos disponibles.
    - Responde: Lista de ProductoRead

-   GET /productos/{producto_id}

    - Descripción: Obtiene un producto por su ID.
    - Parámetros: producto_id (ID del producto)
    - Responde: ProductoRead (producto encontrado)

-   PUT /productos/{producto_id}

    - Descripción: Actualiza los detalles de un producto.
    - Parámetros: producto_id (ID del producto a actualizar), ProductoUpdate (campos a actualizar)
    - Responde: ProductoRead (producto actualizado)

-   DELETE /productos/{producto_id}

    - Descripción: Elimina un producto.
    - Parámetros: producto_id (ID del producto a eliminar)
    - Responde: ProductoRead (producto eliminado)

### Endpoints de Orden:

-   POST /ordenes/

    - Descripción: Crea una nueva orden de compra.
    - Requiere: OrdenCreate (incluye estado, total, usuario_id, y detalles de la orden)
    - Responde: OrdenRead (orden creada)

-   GET /ordenes/

    - Descripción: Obtiene todas las órdenes de compra.
    - Responde: Lista de OrdenRead

-   GET /ordenes/{orden_id}

    - Descripción: Obtiene una orden por su ID.
    - Parámetros: orden_id (ID de la orden)
    - Responde: OrdenRead (orden encontrada)

-   PUT /ordenes/{orden_id}

    - Descripción: Actualiza los detalles de una orden.
    - Parámetros: orden_id (ID de la orden a actualizar), OrdenUpdate (campos a actualizar)
    - Responde: OrdenRead (orden actualizada)

-   DELETE /ordenes/{orden_id}

    - Descripción: Elimina una orden.
    - Parámetros: orden_id (ID de la orden a eliminar)
    - Responde: OrdenRead (orden eliminada)

### Endpoints de Review (Reseñas):

-   POST /reviews/{producto_id}

    - Descripción: Crea una reseña para un producto.
    - Parámetros: producto_id (ID del producto), ReviewCreate (contenido de la reseña)
    - Responde: ReviewRead (reseña creada)

-   POST /reviews/{evento_id}

    - Descripción: Crea una reseña para un evento.
    - Parámetros: evento_id (ID del evento), ReviewCreate (contenido de la reseña)
    - Responde: ReviewRead (reseña creada)

-   GET /reviews/{producto_id}

    - Descripción: Obtiene todas las reseñas de un producto.
    - Parámetros: producto_id (ID del producto)
    - Responde: Lista de ReviewRead

-   GET /reviews/{evento_id}

    - Descripción: Obtiene todas las reseñas de un evento.
    - Parámetros: evento_id (ID del evento)
    - Responde: Lista de ReviewRead

-   DELETE /reviews/{review_id}

    - Descripción: Elimina una reseña de un producto o evento.
    - Parámetros: review_id (ID de la reseña a eliminar), usuario_id (ID del usuario que creó la reseña)
    - Responde: ReviewRead (reseña eliminada)

### Endpoints de Evento:

-   POST /eventos/

    - Descripción: Crea un nuevo evento.
    - Requiere: EventoCreate (detalles del evento)
    - Responde: EventoRead (evento creado)
    
-   GET /eventos/

    - Descripción: Obtiene todos los eventos disponibles.
    - Responde: Lista de EventoRead

-   GET /eventos/{evento_id}

    - Descripción: Obtiene un evento por su ID.
    - Parámetros: evento_id (ID del evento)
    - Responde: EventoRead (evento encontrado)

-   PUT /eventos/{evento_id}

    - Descripción: Actualiza los detalles de un evento.
    - Parámetros: evento_id (ID del evento a actualizar), EventoUpdate (campos a actualizar)
    - Responde: EventoRead (evento actualizado)

-   DELETE /eventos/{evento_id}

    - Descripción: Elimina un evento.
    - Parámetros: evento_id (ID del evento a eliminar)
    - Responde: EventoRead (evento eliminado)

### Endpoints de Compartido:

-   POST /compartidos/

    - Descripción: Crea un registro de "compartido", es decir, compartir un producto o evento con un amigo.
    - Requiere: CompartidoCreate (detalles del "compartido")
    - Responde: CompartidoRead (compartido creado)

### Endpoints de Usuario:

-   POST /usuarios/{usuario_id}/amistad/{amigo_id}

    - Descripción: Establece una relación de amistad entre dos usuarios.
    - Parámetros: usuario_id (ID del usuario que hace la solicitud), amigo_id (ID del usuario al que se desea agregar como amigo)
    - Responde: AmistadRead (relación de amistad establecida)

-   DELETE /usuarios/{usuario_id}/amistad/{amigo_id}

    - Descripción: Elimina una relación de amistad entre dos usuarios.
    - Parámetros: usuario_id (ID del usuario que solicita eliminar la amistad), amigo_id (ID del amigo a eliminar)
    - Responde: AmistadRead (relación de amistad eliminada)
