CREATE TABLE usuario (
    id integer generated always as identity primary key,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100),
    fecha_nac DATE,
    dni VARCHAR(9) UNIQUE,
    email VARCHAR(100),
    nacionalidad varchar(50),
    telefono VARCHAR(20),
    direccion VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE estado (
    id integer generated always as identity primary key,
    descripcion VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE tasacion (
    id integer generated always as identity primary key,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id),
    fecha DATE NOT NULL,
    peso_gramos numeric(10,2) not null,
    valor NUMERIC(12,2) NOT NULL,  -- precio oro del día
    importe numeric(12,2) default 0
);

CREATE TABLE venta (
    id integer generated always as identity primary key,
    usuario_id INTEGER NOT NULL REFERENCES usuario(id),
    estado_id INTEGER NOT NULL REFERENCES estado(id),
    precio NUMERIC(12,2) NOT NULL,
    id_tasacion INTEGER NOT NULL REFERENCES tasacion(id),
    gramos NUMERIC(10,2) NOT NULL
);

--Insertamos estados
INSERT INTO estado (descripcion) VALUES
('TASACION'),
('ACEPTADA'),
('RECHAZADA');

