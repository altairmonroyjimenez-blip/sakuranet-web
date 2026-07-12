-- Crear base de datos
CREATE DATABASE IF NOT EXISTS sakuranet;
USE sakuranet;

-- Tabla categorias
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla productos
-- Incluye imagen con fondo y sin fondo
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2),
    stock INT,
    imagen_con_fondo VARCHAR(255),   -- imagen original con fondo
    imagen_sin_fondo VARCHAR(255),   -- imagen procesada sin fondo
    id_categoria INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

-- Tabla ventas (para producto del mes y más vendidos)
CREATE TABLE IF NOT EXISTS ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    cantidad INT,
    fecha_venta DATETIME,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla producto_del_mes
CREATE TABLE IF NOT EXISTS producto_del_mes (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    mes INT,
    año INT,
    fecha_asignado DATETIME,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla productos_destacados
CREATE TABLE IF NOT EXISTS productos_destacados (
    id_destacado INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    prioridad INT,
    activo BOOLEAN,
    fecha_asignado DATETIME,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Tabla solicitudes
CREATE TABLE IF NOT EXISTS solicitudes (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150),
    telefono VARCHAR(20),
    correo VARCHAR(150),
    direccion TEXT,
    servicio VARCHAR(100),
    estatus VARCHAR(50),
    fecha DATETIME
);

-- Tabla paquetes_internet
CREATE TABLE IF NOT EXISTS paquetes_internet (
    id_paquete INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    velocidad VARCHAR(50),
    precio DECIMAL(10,2),
    descripcion TEXT,
    estado BOOLEAN
);

-- Tabla streaming
CREATE TABLE IF NOT EXISTS streaming (
    id_streaming INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    precio DECIMAL(10,2),
    descripcion TEXT,
    imagen VARCHAR(255),
    estado BOOLEAN
);

-- Tabla administradores
-- Incluye nombre y rol como pediste
CREATE TABLE IF NOT EXISTS administradores (
    id_admin INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50),
    password VARCHAR(255),
    nombre VARCHAR(150),
    rol VARCHAR(50)
);

-- Datos de prueba

INSERT INTO categorias (nombre) VALUES
('Papelería'),
('Electrónica');

INSERT INTO productos
(nombre, descripcion, precio, stock, imagen_con_fondo, imagen_sin_fondo, id_categoria)
VALUES
('Cuaderno Profesional','200 hojas',45,50,'cuaderno_fondo.png','cuaderno_sinfondo.png',1),
('Cable USB Tipo C','Carga rápida',120,30,'cable_fondo.png','cable_sinfondo.png',2);
