use clasificados_db;

-- se agrega una columna a una tabla 

ALTER TABLE publicaciones
	ADD COLUMN titulo CHAR(50);

-- eliminar una tabla
DROP TABLE IF EXISTS contacto