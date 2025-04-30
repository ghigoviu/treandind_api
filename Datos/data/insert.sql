show tables;
desc usuarios ;
create database if not exists plexoweb_treanding_dev;

use plexoweb_treanding_dev;
select * from usuarios;
select * from amistades;
select * from productos;
select * from categorias;
select * from eventos;
select * from evento_asistentes;
select * from producto_imagenes;
select * from producto_atributos;
select * from ordenes;
select * from orden_detalles;
select * from compartidos;

INSERT INTO usuarios (id, nombre, email, password, imagen_perfil, creado_en) VALUES
(1, 'Carlos Mendoza', 'carlos@example.com', 'hash_password_1', 'https://randomuser.me/api/portraits/men/1.jpg', '2024-01-10 14:30:00'),
(2, 'Ana Gómez', 'ana@example.com', 'hash_password_2', 'https://randomuser.me/api/portraits/women/2.jpg', '2024-01-12 08:45:00'),
(3, 'Miguel Torres', 'miguel@example.com', 'hash_password_3', 'https://randomuser.me/api/portraits/men/3.jpg', '2024-01-15 11:20:00'),
(4, 'Laura Martínez', 'laura@example.com', 'hash_password_4', 'https://randomuser.me/api/portraits/women/4.jpg', '2024-01-20 16:15:00'),
(5, 'Pedro Sánchez', 'pedro@example.com', 'hash_password_5', 'https://randomuser.me/api/portraits/men/5.jpg', '2024-01-25 09:30:00'),
(6, 'Sofía Rodríguez', 'sofia@example.com', 'hash_password_6', 'https://randomuser.me/api/portraits/women/6.jpg', '2024-02-01 13:45:00'),
(7, 'Lucas García', 'lucas@example.com', 'hash_password_7', 'https://randomuser.me/api/portraits/men/7.jpg', '2024-02-05 10:20:00'),
(8, 'Valentina Díaz', 'valentina@example.com', 'hash_password_8', 'https://randomuser.me/api/portraits/women/8.jpg', '2024-02-10 15:10:00'),
(9, 'Diego López', 'diego@example.com', 'hash_password_9', 'https://randomuser.me/api/portraits/men/9.jpg', '2024-02-15 08:30:00'),
(10, 'Camila Pérez', 'camila@example.com', 'hash_password_10', 'https://randomuser.me/api/portraits/women/10.jpg', '2024-02-20 12:00:00'),
(11, 'Daniela Castro', 'daniela.castro@example.com', SHA2('danielaPass1', 256), 'daniela.jpg', '2024-03-11 09:35:20'),
(12, 'Miguel Navarro', 'miguel.navarro@example.com', SHA2('miguel2024', 256), 'miguel.png', '2024-03-12 10:40:50'),
(13, 'Camila Ortega', 'camila.ortega@example.com', SHA2('camilaSafe!', 256), 'camila.jpg', '2024-03-13 11:25:35'),
(14, 'Andrés Vega', 'andres.vega@example.com', SHA2('vegaSecure', 256), 'andres.jpg', '2024-03-14 14:50:15'),
(15, 'Paula Mendoza', 'paula.mendoza@example.com', SHA2('paulaKey987', 256), 'paula.png', '2024-03-15 16:05:10'),
(16, 'Sebastián Lara', 'sebastian.lara@example.com', SHA2('sebastianPass', 256), 'sebastian.jpg', '2024-03-16 17:45:00'),
(17, 'Valentina Ríos', 'valentina.rios@example.com', SHA2('valen1234', 256), 'valentina.png', '2024-03-17 08:30:30'),
(18, 'Diego Acosta', 'diego.acosta@example.com', SHA2('dieguito456', 256), 'diego.jpg', '2024-03-18 13:10:25'),
(19, 'Isabella León', 'isabella.leon@example.com', SHA2('isaL3onPass', 256), 'isabella.jpg', '2024-03-19 15:55:40'),
(20, 'Mateo Cabrera', 'mateo.cabrera@example.com', SHA2('mateoSecure!', 256), 'mateo.png', '2024-03-20 19:20:10');

INSERT INTO amistades (id, usuario_id, amigo_id, estado, creado_en) VALUES
(1, 1, 2, 'aceptada', '2024-02-15 10:30:00'),
(2, 1, 3, 'aceptada', '2024-02-20 14:45:00'),
(3, 2, 4, 'aceptada', '2024-02-25 09:15:00'),
(4, 3, 5, 'aceptada', '2024-03-01 16:20:00'),
(5, 4, 6, 'pendiente', '2024-03-05 11:40:00'),
(6, 5, 7, 'aceptada', '2024-03-10 13:25:00'),
(7, 6, 8, 'rechazada', '2024-03-15 10:10:00'),
(8, 7, 9, 'aceptada', '2024-03-20 15:55:00'),
(9, 8, 10, 'pendiente', '2024-03-25 12:30:00'),
(10, 9, 1, 'aceptada', '2024-04-01 09:45:00');

INSERT INTO categorias (id, nombre, descripcion) VALUES
(1, 'Tecnología', 'Dispositivos electrónicos y gadgets' ),
(2, 'Moda', 'Ropa y accesorios de vestir'),
(3, 'Cocina', 'Utensilios y equipamiento para cocina'),
(4, 'Deportes', 'Equipamiento y artículos deportivos'),
(5, 'Libros', 'Ficción, no ficción y más'),
(6, 'Belleza', 'Productos de maquillaje y cuidado personal'),
(7, 'Hogar', 'Artículos para el hogar y decoración'),
(8, 'Bebidas', 'Licores y bebidas especiales'),
(9, 'Mascotas', 'Accesorios y productos para animales'),
(10, 'Música', 'Instrumentos y accesorios musicales');

INSERT INTO productos (id, nombre, descripcion, precio, stock, usuario_id, categoria_id, requiere_edad, calificacion, creado_en) VALUES
(1, 'Smartphone Galaxy S20', 'Teléfono móvil de alta gama con cámara de 64MP', 699.99, 45, 1, 1, false, 4.7, '2024-02-25 10:00:00'),
(2, 'Chaqueta de cuero', 'Chaqueta de cuero genuino para hombre', 189.99, 20, 2, 2, false, 4.5, '2024-02-26 11:15:00'),
(3, 'Juego de sartenes antiadherentes', 'Set de 3 sartenes con revestimiento cerámico', 75.50, 15, 3, 3, false, 4.8, '2024-03-01 09:30:00'),
(4, 'Balón de fútbol profesional', 'Balón oficial de competición', 49.99, 30, 4, 4, false, 4.6, '2024-03-05 14:20:00'),
(5, 'Whisky Premium', 'Whisky escocés añejado 18 años', 120.00, 10, 5, 8, true, 4.9, '2024-03-10 16:45:00'),
(6, 'Novela ''El laberinto de los espíritus''', 'Última entrega de la saga del Cementerio de los Libros Olvidados', 24.99, 50, 6, 5, false, 4.7, '2024-03-15 11:30:00'),
(7, 'Set de maquillaje profesional', 'Kit completo con sombras, bases y brochas', 89.99, 25, 7, 6, false, 4.4, '2024-03-20 13:15:00'),
(8, 'Drone con cámara HD', 'Drone controlado por app con cámara de alta definición', 299.99, 12, 8, 1, false, 4.6, '2024-03-25 10:45:00'),
(9, 'Guitarra acústica', 'Guitarra de concierto con cuerdas de nylon', 159.99, 8, 9, 10, false, 4.8, '2024-04-01 09:00:00'),
(10, 'Cama para mascota', 'Cama acolchada para perros medianos', 45.50, 18, 10, 9, false, 4.5, '2024-04-05 15:30:00');

INSERT INTO producto_imagenes (id, producto_id, url, es_portada) VALUES
(1, 1, "https://placehold.co/600x400", true),
(2, 1, "https://placehold.co/600x400", false),
(3, 1, "https://placehold.co/600x400", false),
(4, 2, "https://placehold.co/600x400", true),
(5, 2, "https://placehold.co/600x400", false),
(6, 2, "https://placehold.co/600x400", false),
(7, 3, "https://placehold.co/600x400", true),
(8, 3, "https://placehold.co/600x400", false),
(9, 3, "https://placehold.co/600x400", false),
(10, 4, "https://placehold.co/600x400", true),
(11, 4, "https://placehold.co/600x400", false),
(12, 4, "https://placehold.co/600x400", false),
(13, 5, "https://placehold.co/600x400", true),
(14, 5, "https://placehold.co/600x400", false),
(15, 5, "https://placehold.co/600x400", false),
(16, 6, "https://placehold.co/600x400", true),
(17, 6, "https://placehold.co/600x400", true),
(18, 6, "https://placehold.co/600x400", false),
(19, 6, "https://placehold.co/600x400", false),
(20, 7, "https://placehold.co/600x400", true),
(21, 7, "https://placehold.co/600x400", false),
(22, 7, "https://placehold.co/600x400", false),
(23, 7, "https://placehold.co/600x400", false),
(24, 8, "https://placehold.co/600x400", true),
(25, 8, "https://placehold.co/600x400", false),
(26, 8, "https://placehold.co/600x400", false),
(27, 8, "https://placehold.co/600x400", false),
(28, 9, "https://placehold.co/600x400", true),
(29, 9, "https://placehold.co/600x400", false),
(30, 9, "https://placehold.co/600x400", false),
(31, 9, "https://placehold.co/600x400", false),
(32, 10, "https://placehold.co/600x400", true),
(33, 10, "https://placehold.co/600x400", false),
(34, 10, "https://placehold.co/600x400", false),
(35, 10, "https://placehold.co/600x400", false);

INSERT INTO producto_atributos (id, producto_id, nombre, valor) VALUES
(1, 1, 'Color', 'Negro'),
(2, 1, 'Memoria', '128GB'),
(3, 1, 'Dual SIM', 'Sí'),
(4, 2, 'Talla', 'M'),
(5, 2, 'Color', 'Marrón'),
(6, 3, 'Material', 'Aluminio'),
(7, 4, 'Tamaño', '5'),
(8, 5, 'Volumen', '750ml'),
(9, 8, 'Autonomía', '30 minutos'),
(10, 9, 'Tipo', 'Clásica');

INSERT INTO eventos (id, usuario_id, nombre, precio, descripcion, categoria, fecha, ubicacion, img_evento, calificacion, creado_en) VALUES
(1, 1, 'Conferencia de Tecnología', 50.00, 'Última tendencias en tecnología e innovación', 'Evento', '2025-05-15 09:00:00', 'Centro de Convenciones, Madrid', 'https://example.com/images/events/tech_conference.jpg', 4.6, '2024-03-01 14:30:00'),
(2, 2, 'Concierto benéfico', 25.00, 'Evento musical solidario para recaudar fondos', 'Charity', '2025-05-20 20:00:00', 'Teatro Principal, Barcelona', 'https://example.com/images/events/charity_concert.jpg', 4.8, '2024-03-05 11:45:00'),
(3, 3, 'Tour gastronómico', 35.00, 'Recorrido por los mejores restaurantes de la ciudad', 'Expirience of the day', '2025-05-25 12:00:00', 'Casco histórico, Valencia', 'https://example.com/images/events/food_tour.jpg', 4.9, '2024-03-10 09:20:00'),
(4, 4, 'Torneo de videojuegos', 15.00, 'Competición amateur de Fortnite y League of Legends', 'Gameplay', '2025-06-01 16:00:00', 'Arena Gaming, Sevilla', 'https://example.com/images/events/gaming_tournament.jpg', 4.5, '2024-03-15 16:15:00'),
(5, 5, 'Workshop de fotografía', 40.00, 'Taller práctico de fotografía urbana', 'Expirience of the day', '2025-06-05 10:00:00', 'Estudio Central, Málaga', 'https://example.com/images/events/photo_workshop.jpg', 4.7, '2024-03-20 13:30:00'),
(6, 6, 'Maratón solidaria', 20.00, 'Carrera benéfica de 10km', 'Charity', '2025-06-10 08:00:00', 'Parque Central, Bilbao', 'https://example.com/images/events/charity_marathon.jpg', 4.4, '2024-03-25 10:45:00'),
(7, 7, 'Exposición de arte contemporáneo', 10.00, 'Muestra de artistas nacionales emergentes', 'Evento', '2025-06-15 11:00:00', 'Galería Moderna, Zaragoza', 'https://example.com/images/events/art_exhibition.jpg', 4.6, '2024-04-01 15:20:00'),
(8, 8, 'Festival de cine independiente', 30.00, 'Proyección de cortometrajes y debate', 'Evento', '2025-06-20 19:00:00', 'Cine Clásico, Alicante', 'https://example.com/images/events/film_festival.jpg', 4.5, '2024-04-05 12:10:00'),
(9, 9, 'Streaming de FIFA 25', 5.00, 'Partido online comentado por jugadores profesionales', 'Gameplay', '2025-06-25 21:00:00', 'Virtual', 'https://example.com/images/events/fifa_stream.jpg', 4.3, '2024-04-10 17:45:00'),
(10, 10, 'Clase de cocina italiana', 45.00, 'Aprende a preparar pasta fresca y salsas caseras', 'Expirience of the day', '2025-06-30 18:00:00', 'Escuela Culinaria, Murcia', 'https://example.com/images/events/cooking_class.jpg', 4.9, '2024-04-15 14:30:00');

INSERT INTO eventos (id, usuario_id, nombre, precio, descripcion, categoria, fecha, ubicacion, img_evento, calificacion, creado_en) VALUES
(1, 1, 'Conferencia de Tecnología', 50.00, 'Última tendencias en tecnología e innovación', 'Evento', '2025-05-15 09:00:00', 'Centro de Convenciones, Madrid', 'https://example.com/images/events/tech_conference.jpg', 4.6, '2024-03-01 14:30:00'),
(2, 2, 'Concierto benéfico', 25.00, 'Evento musical solidario para recaudar fondos', 'Charity', '2025-05-20 20:00:00', 'Teatro Principal, Barcelona', 'https://example.com/images/events/charity_concert.jpg', 4.8, '2024-03-05 11:45:00'),
(3, 3, 'Tour gastronómico', 35.00, 'Recorrido por los mejores restaurantes de la ciudad', 'Expirience of the day', '2025-05-25 12:00:00', 'Casco histórico, Valencia', 'https://example.com/images/events/food_tour.jpg', 4.9, '2024-03-10 09:20:00'),
(4, 4, 'Torneo de videojuegos', 15.00, 'Competición amateur de Fortnite y League of Legends', 'Gameplay', '2025-06-01 16:00:00', 'Arena Gaming, Sevilla', 'https://example.com/images/events/gaming_tournament.jpg', 4.5, '2024-03-15 16:15:00'),
(5, 5, 'Workshop de fotografía', 40.00, 'Taller práctico de fotografía urbana', 'Expirience of the day', '2025-06-05 10:00:00', 'Estudio Central, Málaga', 'https://example.com/images/events/photo_workshop.jpg', 4.7, '2024-03-20 13:30:00'),
(6, 6, 'Maratón solidaria', 20.00, 'Carrera benéfica de 10km', 'Charity', '2025-06-10 08:00:00', 'Parque Central, Bilbao', 'https://example.com/images/events/charity_marathon.jpg', 4.4, '2024-03-25 10:45:00'),
(7, 7, 'Exposición de arte contemporáneo', 10.00, 'Muestra de artistas nacionales emergentes', 'Evento', '2025-06-15 11:00:00', 'Galería Moderna, Zaragoza', 'https://example.com/images/events/art_exhibition.jpg', 4.6, '2024-04-01 15:20:00'),
(8, 8, 'Festival de cine independiente', 30.00, 'Proyección de cortometrajes y debate', 'Evento', '2025-06-20 19:00:00', 'Cine Clásico, Alicante', 'https://example.com/images/events/film_festival.jpg', 4.5, '2024-04-05 12:10:00'),
(9, 9, 'Streaming de FIFA 25', 5.00, 'Partido online comentado por jugadores profesionales', 'Gameplay', '2025-06-25 21:00:00', 'Virtual', 'https://example.com/images/events/fifa_stream.jpg', 4.3, '2024-04-10 17:45:00'),
(10, 10, 'Clase de cocina italiana', 45.00, 'Aprende a preparar pasta fresca y salsas caseras', 'Expirience of the day', '2025-06-30 18:00:00', 'Escuela Culinaria, Murcia', 'https://example.com/images/events/cooking_class.jpg', 4.9, '2024-04-15 14:30:00');

INSERT INTO evento_asistentes (id, evento_id, usuario_id, estado, creado_en) VALUES
(1, 1, 3, 'confirmada', '2024-04-01 10:15:00'),
(2, 1, 5, 'confirmada', '2024-04-02 14:30:00'),
(3, 2, 1, 'pendiente', '2024-04-05 09:45:00'),
(4, 2, 7, 'confirmada', '2024-04-06 16:20:00'),
(5, 3, 2, 'confirmada', '2024-04-10 11:10:00'),
(6, 4, 6, 'cancelada', '2024-04-12 15:40:00'),
(7, 5, 8, 'confirmada', '2024-04-15 13:25:00'),
(8, 6, 9, 'pendiente', '2024-04-18 10:50:00'),
(9, 7, 10, 'confirmada', '2024-04-20 14:15:00'),
(10, 8, 4, 'confirmada', '2024-04-22 17:30:00');

INSERT INTO reviews (id, producto_id, evento_id, usuario_id, calificacion, comentario, creado_en) VALUES
(1, 1, NULL, 3, 5, 'Excelente smartphone, muy rápido y con una cámara increíble', '2024-03-10 16:45:00'),
(2, 1, NULL, 5, 4, 'Buen teléfono, aunque la batería podría durar un poco más', '2024-03-15 09:30:00'),
(3, 2, NULL, 7, 5, 'La chaqueta es de excelente calidad, tal como se muestra en las fotos', '2024-03-20 14:15:00'),
(4, NULL, 1, 2, 4, 'Conferencia muy interesante con buenos ponentes', '2024-05-16 18:00:00'),
(5, NULL, 1, 4, 5, 'Increíble organización y contenido de primer nivel', '2024-05-17 10:30:00'),
(6, 5, NULL, 8, 5, 'El mejor whisky que he probado en años', '2024-03-25 20:45:00'),
(7, NULL, 3, 1, 5, 'Una experiencia gastronómica inolvidable', '2024-05-26 14:20:00'),
(8, 8, NULL, 10, 4, 'El drone funciona muy bien, aunque el control podría ser más intuitivo', '2024-04-05 11:10:00'),
(9, NULL, 5, 6, 5, 'Workshop muy completo, aprendí muchísimo', '2024-06-06 16:30:00'),
(10, 10, NULL, 9, 4, 'Mi perro está encantado con su nueva cama', '2024-04-15 13:45:00');

INSERT INTO ordenes (id, usuario_id, estado, total, creado_en) VALUES
(1, 3, 'completado', 150.00, '2025-04-01T10:23:00'),
(2, 5, 'pendiente', 80.50, '2025-04-03T14:05:00'),
(3, 1, 'cancelado', 0.00, '2025-04-04T09:00:00'),
(4, 7, 'completado', 210.75, '2025-04-05T16:15:00'),
(5, 2, 'completado', 65.00, '2025-04-06T11:30:00'),
(6, 4, 'pendiente', 99.99, '2025-04-07T18:45:00'),
(7, 8, 'en_proceso', 120.00, '2025-04-08T13:20:00'),
(8, 6, 'completado', 45.50, '2025-04-10T09:50:00'),
(9, 10, 'cancelado', 0.00, '2025-04-11T12:00:00'),
(10, 9, 'completado', 185.25, '2025-04-12T17:10:00');

INSERT INTO orden_detalles (id, orden_id, producto_id, evento_id, cantidad, precio_unit) VALUES
(1, 1, 2, NULL, 2, 30.00),
(2, 2, NULL, 1, 1, 80.50),
(3, 4, 3, NULL, 5, 42.15),
(4, 5, 5, NULL, 1, 65.00),
(5, 6, NULL, 2, 2, 49.99),
(6, 7, 7, NULL, 3, 40.00),
(7, 8, NULL, 3, 1, 45.50),
(8, 10, 9, NULL, 3, 61.75),
(9, 10, 6, NULL, 1, 0.00),
(10, 7, NULL, 4, 1, 60.00);

INSERT INTO compartidos (id, usuario_id, producto_id, evento_id, amigo_id, mensaje, creado_en) VALUES
(1, 1, 3, NULL, 5, '¡Te recomiendo este producto!', '2025-04-01T09:00:00'),
(2, 2, NULL, 1, 4, 'Este evento te va a encantar.', '2025-04-02T12:15:00'),
(3, 3, 7, NULL, 6, 'Mira esto que compré.', '2025-04-03T08:30:00'),
(4, 4, NULL, 3, 2, 'Nos vemos ahí, ¿no?', '2025-04-04T15:40:00'),
(5, 5, 1, NULL, 1, 'Está buenísimo.', '2025-04-05T11:00:00'),
(6, 6, NULL, 2, 9, 'Deberías asistir.', '2025-04-06T17:25:00'),
(7, 7, 8, NULL, 10, 'Me encantó, pruébalo.', '2025-04-07T10:50:00'),
(8, 8, NULL, 5, 3, 'Va a estar buenísimo.', '2025-04-08T13:35:00'),
(9, 9, 4, NULL, 7, 'Te va a gustar este producto.', '2025-04-09T19:10:00'),
(10, 10, NULL, 4, 8, 'Vamos juntos.', '2025-04-10T16:00:00');
