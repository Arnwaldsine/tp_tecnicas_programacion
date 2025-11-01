# Queries para crear y poblar la base de datos (crear_base.py importará estas variables)
CREATE_MARCAS_TABLE = """
CREATE TABLE IF NOT EXISTS marcas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT
)
"""

CREATE_TIPOS_TABLE = """
CREATE TABLE IF NOT EXISTS tipos_producto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT
)
"""

CREATE_PRODUCTOS_TABLE = """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelo TEXT NOT NULL UNIQUE,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    ventas INTEGER NOT NULL DEFAULT 0,
    marca_id INTEGER NOT NULL,
    tipo_id INTEGER NOT NULL,
    FOREIGN KEY (marca_id) REFERENCES marcas(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (tipo_id) REFERENCES tipos_producto(id) ON DELETE CASCADE ON UPDATE CASCADE
)
"""

# Datos iniciales (listas de tuplas) para insertar
MARCAS_INICIALES = [
    ('Dell', 'Notebooks Dell'),
    ('Asus', 'Notebooks Asus'),
    ('HP', 'Notebooks HP'),
    ('Motorola', 'Celulares Motorola'),
    ('Samsung', 'Celulares Samsung'),
    ('Xiaomi', 'Celulares y relojes Xiaomi'),
    ('Casio', 'Relojes Casio'),
]

TIPOS_INICIALES = [
    ('Notebook', 'Computadoras portátiles'),
    ('Celular', 'Teléfonos móviles'),
    ('Reloj', 'Relojes inteligentes o analógicos'),
]

PRODUCTOS_INICIALES = [
    ('Inspiron 15 3000', 650.00, 15, 0),
    ('XPS 13', 1200.00, 10, 0),
    ('Latitude 7420', 1400.00, 8, 0),
    ('ZenBook 14', 900.00, 12, 0),
    ('VivoBook 15', 700.00, 9, 0),
    ('ROG Strix G15', 1500.00, 7, 0),
    ('Pavilion 15', 680.00, 14, 0),
    ('Envy x360', 1050.00, 11, 0),
    ('Spectre x360', 1350.00, 6, 0),
    ('Moto G Power (2023)', 200.00, 25, 0),
    ('Moto G Stylus', 280.00, 20, 0),
    ('Moto Edge 30', 450.00, 15, 0),
    ('Galaxy A53', 350.00, 18, 0),
    ('Galaxy S21', 650.00, 12, 0),
    ('Galaxy S23', 900.00, 8, 0),
    ('Redmi Note 11', 220.00, 22, 0),
    ('Xiaomi 11T', 420.00, 16, 0),
    ('Redmi 12', 180.00, 10, 0),
    ('Mi Band 6', 45.00, 30, 0),
    ('Mi Watch Lite', 60.00, 25, 0),
    ('Redmi Watch 2', 100.00, 20, 0),
    ('G-Shock GA-2100', 120.00, 28, 0),
    ('Casio F-91W', 25.00, 22, 0),
    ('Edifice EFV-100', 80.00, 18, 0),
]

# Sentencias parametrizadas para inserciones (usadas con cursor.executemany)
INSERT_MARCA = "INSERT OR IGNORE INTO marcas (nombre, descripcion) VALUES (?, ?)"
INSERT_TIPO = "INSERT OR IGNORE INTO tipos_producto (nombre, descripcion) VALUES (?, ?)"
INSERT_PRODUCTO = """
INSERT OR IGNORE INTO productos (modelo, precio, stock, ventas, marca_id, tipo_id)
VALUES (?, ?, ?, ?, ?, ?)
"""