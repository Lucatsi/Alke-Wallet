# 🏦 Proyecto Alke Wallet - Base de Datos Relacional

Este repositorio contiene la implementación y diseño de la base de datos relacional para **Alke Wallet**, un sistema de billetera virtual que permite a los usuarios almacenar fondos, realizar transacciones y consultar historiales.

Este proyecto fue desarrollado como parte de la evaluación integradora del módulo **"Fundamentos de bases de datos relacionales"**.

## 🎯 Objetivo General
Diseñar el modelo conceptual, definir las relaciones entre entidades y crear la base de datos en SQL para garantizar la coherencia y la integridad de la información financiera de la wallet, cumpliendo con los principios **ACID** (Atomicidad, Consistencia, Aislamiento y Durabilidad).

## 🛠️ Tecnologías y Herramientas Utilizadas
- **Lenguaje:** SQL (MySQL 8 / MariaDB)
- **Gestor de Base de Datos / Cliente:** HeidiSQL / VS Code (SQLTools)
- **Modelado ER:** Mermaid / Draw.io

## 🗂️ Estructura de Archivos
- `AlkeWallet.sql`: Script principal que contiene todas las sentencias DDL (creación de tablas, claves primarias y foráneas, índices) y DML (inserción de datos, transacciones y consultas específicas).
- `Entregable_AlkeWallet.md`: Archivo con la estructura y respuestas de las consultas SQL, listo para ser utilizado como base para el documento entregable (Word).
- `diagrama_erk.md`: Código en formato Mermaid del Diagrama Entidad-Relación (ER) normalizado en 3FN.

## 🗃️ Modelo de Datos (Entidades Principales)
1. **Usuario:** Almacena los datos personales y el saldo de cada usuario (`user_id`, `nombre`, `correo_electronico`, `contrasena`, `saldo`, `fecha_creacion`).
2. **Moneda:** Catálogo de divisas soportadas por la billetera (`currency_id`, `currency_name`, `currency_symbol`).
3. **Transaccion:** Registro histórico y trazabilidad de los movimientos financieros entre los usuarios (`transaction_id`, `sender_user_id`, `receiver_user_id`, `importe`, `transaction_date`, `currency_id`).

## 🚀 Funcionalidades Implementadas (SQL)
- Creación de esquema y tablas relacionales (`CREATE TABLE`, `ALTER TABLE`, `INDEX`).
- Control de Integridad Referencial (`FOREIGN KEY`, restricciones `ON DELETE CASCADE` y `RESTRICT`).
- Inserción masiva de datos de prueba (`INSERT INTO`).
- Consultas relacionales complejas usando sub-consultas y múltiples `JOIN`.
- Modificación y eliminación de registros específicos (`UPDATE`, `DELETE`).
- Protección de inconsistencias mediante transaccionalidad (`START TRANSACTION`, `COMMIT`, `ROLLBACK`).
- Creación de Vistas y funciones de agregación (`COUNT`, `ORDER BY`, `CREATE VIEW`).

## ⚙️ Instrucciones de Ejecución
1. Abrir **HeidiSQL** (o cualquier cliente MySQL preferido) y conectarse al servidor local.
2. Cargar el archivo `AlkeWallet.sql` (Archivo > Cargar archivo SQL).
3. Ejecutar el script (tecla F9) para crear la base de datos `AlkeWallet`, generar las tablas e insertar los datos iniciales.
4. (Opcional) Visualizar el diagrama de base de datos abriendo el código de `diagrama_erk.md` en [Mermaid Live Editor](https://mermaid.live).

---
*✨ Desarrollado para la evaluación del módulo de Bases de Datos Relacionales.*
