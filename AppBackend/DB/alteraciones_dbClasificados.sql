use clasificados_db;

-- se agrega una columna a una tabla 

ALTER TABLE publicaciones
	ADD COLUMN titulo CHAR(50);

-- eliminar una tabla
DROP TABLE IF EXISTS contacto;

-- eliminar columna
AlTER TABLE contenido
	DROP FOREIGN KEY contenido_ibfk_1,
	DROP COLUMN idpublicacion;
    
ALTER TABLE publicaciones
	ADD COLUMN fechfin DATETIME;
    
ALTER TABLE publicaciones
	CHANGE COLUMN contenido contenido INT;
    
ALTER TABLE publicaciones
	DROP FOREIGN KEY publicaciones_ibfk_3;