-- DB app
CREATE DATABASE clasificados_db;
USE clasificados_db;

-- comandos DDl para crear las tablas

-- Creación de tablas 
-- 1
CREATE TABLE usuarios(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nombres CHAR(60),
    apellidos CHAR(60),
    telefono CHAR(20),
    correo CHAR(40),
    password CHAR(40),
    esadmin BOOLEAN,
    estado BOOLEAN
);
-- 2
CREATE TABLE publicaciones(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    fechinicial DATETIME,
    ciudad CHAR(40),
    precio DOUBLE,
    contacto CHAR(50),
    contenido VARCHAR(500),
    titulo CHAR(50),
    idusuario INT,
    estado BOOLEAN
);
-- 3
CREATE TABLE imagenes(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    idpublicacion INT,
    imagen BLOB
);
-- 4
CREATE TABLE contenido(
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    idpublicacion INT, 
    tipoinmueble CHAR(20),
    metroscuadrados DOUBLE,
    habitaciones CHAR(20),
    banos CHAR(15),
    pisos CHAR(15),
    descripcion VARCHAR(4000)
);


-- FK 
ALTER TABLE publicaciones
	ADD FOREIGN KEY (idusuario) REFERENCES usuarios (id);
    
ALTER TABLE imagenes
	ADD FOREIGN KEY (idpublicacion) REFERENCES publicaciones(id);
    
ALTER TABLE contenido
	ADD FOREIGN KEY (idpublicacion) REFERENCES publicaciones(id);
    