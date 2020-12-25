INSERT INTO usuarios VALUES (1, 'test1@db.com', 'test');
INSERT INTO usuarios VALUES (2, 'test2@db.com', 'test');
INSERT INTO usuarios VALUES (3, 'test3@db.com', 'test');
INSERT INTO usuarios VALUES (4, 'test4@db.com', 'test');
INSERT INTO usuarios VALUES (5, 'test5@db.com', 'test');


INSERT INTO empresas VALUES (1, 'A12345678A','SE1234567890123456789012', 'DIRECCIÓN', 'EMPRESA SA', 123456789, 1);

INSERT INTO personas VALUES (1, 'apellidos', '12345678A', 'cliente', 123456789, 2);
INSERT INTO personas VALUES (2, 'apellidos', '12345678B', 'trabajador',  123456789, 3);
INSERT INTO personas VALUES (3,  'apellidos', '12345678C', 'administrador', 123456789, 4);

INSERT INTO clientes VALUES(1,'SE1234567890123456789012', 'Dirección', 1);

INSERT INTO trabajadores VALUES(1, 'Trabajo1', 2);

INSERT INTO administradores VALUES(1,3);

INSERT INTO plagas VALUES(1, 'Cucarachas');
INSERT INTO plagas VALUES(2, 'Avispas');
INSERT INTO plagas VALUES(3, 'Ratas');

INSERT INTO tratamientos VALUES(1, false, 'Tratamiento contra las cucarachas en zonas exteriores', 0, 'Letal plus cc', 30, 1);
INSERT INTO tratamientos VALUES(2, false, 'Control rutinario de roedores', 0, 'Bloque de veneno', 80, 3);
INSERT INTO tratamientos VALUES(3, false, 'Tratamiento contra las avispas en zonas exteriores', 0, 'Letal plus a', 130, 2);

INSERT INTO solicitud_servicios VALUES(1, '2021-01-01 10:00:00', 3, 'Tengo cucarachas en la cocina', 1, null, 1, 1 );
INSERT INTO solicitud_servicios VALUES(2, '2021-01-01 11:00:00', 3, 'Control rutinario de ratas', null, 1, 3, 2 );
INSERT INTO solicitud_servicios VALUES(3, null, 1, 'Tengo avispas en la jardinera', 1, null, 2, null );
INSERT INTO solicitud_servicios VALUES(4, '2021-01-01 11:00:00', 2, 'Avispas en la verja de entrada', null, 1, 2, 3 );

INSERT INTO servicios VALUES (1,1,null, null, 1, 1);
INSERT INTO servicios VALUES (2,1,null, null, 2, 1);
INSERT INTO servicios VALUES (3,1,null, null, 3, 1);

INSERT INTO vehiculos VALUES (1, '2013-01-01', '2022-01-01', 'Opel', '0001AAA', 'Corsa', 1 )
