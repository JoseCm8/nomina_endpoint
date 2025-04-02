-- Borrado de la base de datos (opcional)
-- drop database nomina;

create database nomina;
use nomina;

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` enum('admin','empleado') NOT NULL DEFAULT 'empleado',
  `fecha_creacion` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

CREATE TABLE `empleados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `dni` varchar(20) NOT NULL,
  `salario_mensual` decimal(10,2) NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `dias_laborados` int(11) NOT NULL,
  `aux_transporte` boolean NOT NULL,
  `fecha_creacion` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `dni` (`dni`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

INSERT INTO `usuarios` (`username`, `nombre`, `email`, `password`, `rol`, `fecha_creacion`)
VALUES ('admin', 'Administrador', 'admin@yopmail.com', '$2a$12$/CaBpkCLyPyJBmB7IN3iNOXet7xfirlNFslbBHwx4nWEl8fewh256', 'admin', '2025-04-01 16:41:15');

INSERT INTO `empleados` (`nombre`, `dni`, `salario_mensual`, `fecha_ingreso`, `dias_laborados`, `aux_transporte`, `fecha_creacion`)
VALUES ('Jose Carrillo', '12345', 1000000.00, '2025-03-31', 30, 1, '2025-04-01 17:49:56');
INSERT INTO `empleados` (`nombre`, `dni`, `salario_mensual`, `fecha_ingreso`, `dias_laborados`, `aux_transporte`, `fecha_creacion`)
VALUES ('Luis Martinez', '56789', 5000000.00, '2025-03-31', 30, 1, '2025-04-01 17:50:51');
