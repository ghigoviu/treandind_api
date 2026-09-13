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
- ✅ CRUD completo para Usuarios, Productos, Eventos, Órdenes y recursos sociales
- ✅ Funciones sociales: amistades, compartidos, reseñas con calificación y colaboraciones
- ✅ Configuración centralizada (env / config.ini) y sesión de BD unificada
- ✅ Tests automatizados con pytest sobre base de datos de pruebas aislada
- ✅ Separación clara entre capas: Controlador (ControladorRest), Repositorio, Modelo, Schema, Datos

---
## ⚙️ Configuración y ejecución

La configuración se centraliza en `Datos/Config.py`, con esta precedencia:
**variables de entorno > `config.ini` > valores por defecto locales**.

`config.ini` (no versionado) de ejemplo:

```ini
[mysql]
user = root
passwd =
host = localhost
port = 3306
db = treanding
echo = false

[host]
add = 127.0.0.1
port = 8081
```

Variables de entorno equivalentes: `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`,
`MYSQL_PORT`, `MYSQL_DB`, `SQL_ECHO`, `API_HOST`, `API_PORT`.

Pasos:

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
python -m Datos.Bulk              # (opcional) carga datos semilla desde Datos/data/*.json
python main.py                    # arranca uvicorn en el host/puerto configurado
```

La documentación interactiva queda en `http://<host>:<port>/docs`.

## 🧪 Tests

Los tests usan `pytest` + `TestClient` de FastAPI contra la base de datos de
pruebas `treanding_test`. Cada test corre en una transacción que se revierte al
finalizar, sin tocar la base de datos de desarrollo.

```bash
python -m pytest -q
```

El esquema de `treanding_test` se crea automáticamente al iniciar la sesión de
tests (fixture `_crear_esquema`).

---
## 🧩 Extensiones posibles

- Autenticación con JWT / OAuth2
- Soporte para roles y permisos
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

Las reseñas validan la calificación en el rango **1-5**, impiden que un mismo
usuario reseñe dos veces el mismo elemento (409) y exigen que se indique
**exactamente uno** de `producto_id` o `evento_id`. El promedio del producto o
evento se recalcula de forma atómica en cada creación, actualización o borrado.

-   POST /reviews/

    - Descripción: Crea una reseña de un producto o evento.
    - Requiere: ReviewCreate (usuario_id, calificacion 1-5, comentario, y producto_id **o** evento_id)
    - Responde: ReviewRead (reseña creada)

-   GET /reviews/producto/{producto_id}

    - Descripción: Obtiene todas las reseñas de un producto.
    - Responde: Lista de ReviewRead

-   GET /reviews/evento/{evento_id}

    - Descripción: Obtiene todas las reseñas de un evento.
    - Responde: Lista de ReviewRead

-   GET /reviews/usuario/{usuario_id}

    - Descripción: Obtiene todas las reseñas hechas por un usuario.
    - Responde: Lista de ReviewRead

-   PUT /reviews/{review_id}

    - Descripción: Actualiza una reseña.
    - Responde: ReviewRead (reseña actualizada)

-   DELETE /reviews/{review_id}/usuario/{usuario_id}

    - Descripción: Elimina una reseña propia (valida propiedad: 403 si no es del usuario).
    - Responde: { "mensaje": "Review eliminado", "id": <review_id> }

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

    - Descripción: Comparte un producto o evento con un amigo. Valida que exista amistad entre ambos usuarios en **cualquier dirección** (403 si no son amigos; 400 si se comparte consigo mismo).
    - Requiere: CompartidoCreate (usuario_id, amigo_id, producto_id o evento_id, mensaje)
    - Responde: CompartidoRead (compartido creado)

-   GET /compartidos/ · GET /compartidos/{compartido_id}

    - Descripción: Lista los compartidos u obtiene uno por ID.

### Endpoints de Amistad:

-   POST /amistades/

    - Descripción: Envía una solicitud de amistad. Impide auto-amistad y duplicados (en ambos sentidos).
    - Requiere: AmistadCreate (usuario_id, amigo_id, estado)
    - Responde: AmistadRead

-   PATCH /amistades/{amistad_id}/estado

    - Descripción: Actualiza el estado de una solicitud (aceptada / rechazada).
    - Responde: AmistadRead

-   GET /amistades/usuario/{usuario_id}

    - Descripción: Amistades aceptadas del usuario (en cualquier dirección).

-   GET /amistades/usuario/{usuario_id}/pendientes

    - Descripción: Solicitudes de amistad pendientes recibidas por el usuario.

-   GET /amistades/usuario/{usuario_id}/detalle

    - Descripción: Usuarios amigos (aceptados) con sus datos (nombre, avatar).

-   GET /amistades/usuario/{usuario_id}/pendientes/detalle

    - Descripción: Solicitudes pendientes recibidas, con datos del solicitante.

-   DELETE /amistades/{amistad_id}

    - Descripción: Elimina una relación de amistad.

### Endpoints de Colaboración:

-   POST /colaboracion/ · PUT /colaboracion/{id} · DELETE /colaboracion/{id}

    - Descripción: CRUD de colaboraciones (desc, img, video, usuario_id del creador).

-   GET /colaboracion/ · GET /colaboracion/{id}

    - Descripción: Lista colaboraciones u obtiene una por ID.

-   GET /colaboracion/{id}/detalle

    - Descripción: Colaboración con creador y miembros enriquecidos (nombre, avatar, porcentaje).

-   GET /colaboracion/usuario/{usuario_id}

    - Descripción: Colaboraciones en las que participa un usuario.

-   POST /colaboracion/{id}/miembros

    - Descripción: Agrega un usuario como miembro (evita duplicados: 400 si ya es miembro).
    - Requiere: { "usuario_id": int, "porcentaje": int }
