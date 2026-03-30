-- ==========================================================
-- PROYECTO: ALKE WALLET (Módulo: Fundamentos de BD Relacionales)
-- ==========================================================

-- 1. CREACIÓN DE LA BASE DE DATOS Y USO
CREATE DATABASE IF NOT EXISTS AlkeWallet;
USE AlkeWallet;

-- 2. DDL: DEFINICIÓN DE TABLAS

-- Creación de la tabla Moneda
CREATE TABLE Moneda (
    currency_id INT AUTO_INCREMENT PRIMARY KEY,
    currency_name VARCHAR(50) NOT NULL,
    currency_symbol VARCHAR(5) NOT NULL
);

-- Creación de la tabla Usuario
CREATE TABLE Usuario (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    saldo DECIMAL(15, 2) NOT NULL DEFAULT 0.00
);

-- Modificar la tabla usuario para añadir la fecha de creación usando ALTER TABLE (Tarea Plus)
ALTER TABLE Usuario 
ADD fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Creación de la tabla Transaccion
CREATE TABLE Transaccion (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_user_id INT NOT NULL,
    receiver_user_id INT NOT NULL,
    importe DECIMAL(15, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    currency_id INT NOT NULL,
    FOREIGN KEY (sender_user_id) REFERENCES Usuario(user_id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_user_id) REFERENCES Usuario(user_id) ON DELETE CASCADE,
    FOREIGN KEY (currency_id) REFERENCES Moneda(currency_id) ON DELETE RESTRICT
);

-- Añadir restricciones NOT NULL e índices compuestos para optimizar búsquedas
CREATE INDEX idx_sender_date ON Transaccion(sender_user_id, transaction_date);
CREATE INDEX idx_receiver_date ON Transaccion(receiver_user_id, transaction_date);


-- 3. DML: INSERCIÓN DE DATOS DE PRUEBA

INSERT INTO Moneda (currency_name, currency_symbol) VALUES 
('Dólar Estadounidense', 'USD'),
('Euro', 'EUR'),
('Peso Chileno', 'CLP'),
('Bitcoin', 'BTC');

INSERT INTO Usuario (nombre, correo_electronico, contrasena, saldo) VALUES 
('Juan Pérez', 'juan.perez@email.com', 'pwd123', 1500.00),
('María Gómez', 'maria.gomez@email.com', 'pwd456', 2500.50),
('Carlos Díaz', 'carlos.diaz@email.com', 'pwd789', 500.00),
('Ana Silva', 'ana.silva@email.com', 'pwd321', 10000.00),
('Luis Torres', 'luis.torres@email.com', 'pwd654', 0.00);

-- Inserción de 5 transacciones de prueba
INSERT INTO Transaccion (sender_user_id, receiver_user_id, importe, currency_id) VALUES 
(1, 2, 100.00, 1),
(2, 3, 50.50, 2),
(4, 1, 200.00, 1),
(3, 5, 20.00, 3),
(1, 4, 150.00, 1);


-- 4. CONSULTAS REQUERIDAS

-- A. Consulta para obtener el nombre de la moneda elegida por un usuario específico (ej: Usuario 1)
SELECT DISTINCT m.currency_name
FROM Transaccion t
JOIN Moneda m ON t.currency_id = m.currency_id
WHERE t.sender_user_id = 1;

-- B. Consulta para obtener todas las transacciones registradas
SELECT * FROM Transaccion;

-- C. Consulta para obtener todas las transacciones realizadas por un usuario específico (enviadas o recibidas, ej: Usuario 1)
SELECT t.transaction_id, t.importe, t.transaction_date, m.currency_symbol,
       s.nombre AS sender_name, r.nombre AS receiver_name
FROM Transaccion t
JOIN Usuario s ON t.sender_user_id = s.user_id
JOIN Usuario r ON t.receiver_user_id = r.user_id
JOIN Moneda m ON t.currency_id = m.currency_id
WHERE t.sender_user_id = 1 OR t.receiver_user_id = 1;

-- D. Sentencia DML para modificar el campo correo electrónico de un usuario específico
UPDATE Usuario
SET correo_electronico = 'nuevo.juan@email.com'
WHERE user_id = 1;

-- E. Sentencia para eliminar los datos de una transacción (eliminado de la fila completa)
DELETE FROM Transaccion
WHERE transaction_id = 5;


-- 5. OTRAS CONSULTAS Y PRÁCTICAS DEL PASO A PASO

-- Explorar objetos básicos
SHOW DATABASES;
SHOW TABLES;
DESCRIBE Usuario;
SHOW CREATE TABLE Transaccion;

-- Ejecutar consultas SELECT básicas y filtros dinámicos con operadores lógicos
SELECT * FROM Usuario WHERE saldo > 1000 AND fecha_creacion IS NOT NULL;

-- Unir las tablas transaccion y usuario mediante INNER JOIN
SELECT u.nombre, t.importe, t.transaction_date 
FROM Usuario u
INNER JOIN Transaccion t ON u.user_id = t.sender_user_id;

-- Practicar sub-consultas para obtener el total de transacciones enviadas por usuario
SELECT u.nombre, 
       (SELECT COUNT(*) FROM Transaccion t WHERE t.sender_user_id = u.user_id) AS total_transacciones_enviadas
FROM Usuario u;

-- Crear una vista que muestre el top-5 de usuarios con mayor saldo
CREATE VIEW Top5Usuarios AS
SELECT nombre, saldo 
FROM Usuario 
ORDER BY saldo DESC 
LIMIT 5;

SELECT * FROM Top5Usuarios;

-- Actualizar el saldo de un usuario luego de una transacción manual
UPDATE Usuario SET saldo = saldo - 100.00 WHERE user_id = 1;
UPDATE Usuario SET saldo = saldo + 100.00 WHERE user_id = 2;

-- Implementar una transacción con START TRANSACTION, COMMIT y ROLLBACK
START TRANSACTION;
INSERT INTO Transaccion (sender_user_id, receiver_user_id, importe, currency_id) VALUES (4, 3, 500.00, 1);
UPDATE Usuario SET saldo = saldo - 500.00 WHERE user_id = 4;
UPDATE Usuario SET saldo = saldo + 500.00 WHERE user_id = 3;
COMMIT;

-- Simular un error de integridad referencial y revertir la operación
START TRANSACTION;
-- (Este insert falla intencionalmente al usar currency_id = 999)
-- INSERT INTO Transaccion (sender_user_id, receiver_user_id, importe, currency_id) VALUES (1, 2, 50.00, 999);
ROLLBACK;
