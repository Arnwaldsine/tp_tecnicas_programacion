import sqlite3

def crear_base_datos():
    """Crea la base de datos y la tabla de productos"""
    
    # Conectar a la base de datos (se crea si no existe)
    conn = sqlite3.connect('inventario.db')
    cursor = conn.cursor()
    
    # Crear la tabla productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            ventas INTEGER NOT NULL DEFAULT 0
        )
    ''')
    
    print("Tabla 'productos' creada exitosamente")
    
    # Insertar datos de ejemplo
    productos_iniciales = [
        # Notebooks Dell
        ('nd1', 850.00, 15, 0),
        ('nd2', 920.00, 10, 0),
        ('nd3', 1100.00, 8, 0),
        # Notebooks Asus
        ('na1', 780.00, 12, 0),
        ('na2', 890.00, 9, 0),
        ('na3', 1050.00, 7, 0),
        # Notebooks HP
        ('nh1', 800.00, 14, 0),
        ('nh2', 950.00, 11, 0),
        ('nh3', 1150.00, 6, 0),
        # Celulares Motorola
        ('cm1', 250.00, 25, 0),
        ('cm2', 320.00, 20, 0),
        ('cm3', 450.00, 15, 0),
        # Celulares Samsung
        ('cs1', 400.00, 18, 0),
        ('cs2', 550.00, 12, 0),
        ('cs3', 750.00, 8, 0),
        # Celulares Xiaomi
        ('cx1', 280.00, 22, 0),
        ('cx2', 380.00, 16, 0),
        ('cx3', 520.00, 10, 0),
        # Relojes Xiaomi
        ('rx1', 80.00, 30, 0),
        ('rx2', 120.00, 25, 0),
        ('rx3', 180.00, 20, 0),
        # Relojes Casio
        ('rc1', 90.00, 28, 0),
        ('rc2', 150.00, 22, 0),
        ('rc3', 220.00, 18, 0),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO productos (nombre, precio, stock, ventas) 
        VALUES (?, ?, ?, ?)
    ''', productos_iniciales)
    
    conn.commit()
    print(f"Se insertaron {len(productos_iniciales)} productos de ejemplo")
    
    # Mostrar todos los productos
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    
    print("\n--- PRODUCTOS EN LA BASE DE DATOS ---")
    print(f"{'ID':<5} {'Modelo':<10} {'Precio':<10} {'Stock':<8} {'Ventas':<8}")
    print("-" * 50)
    for p in productos:
        print(f"{p[0]:<5} {p[1]:<10} ${p[2]:<9.2f} {p[3]:<8} {p[4]:<8}")
    
    conn.close()
    print("\n¡Base de datos creada y poblada exitosamente!")
    print("Ahora puedes ejecutar el sistema de gestión de productos.")

if __name__ == "__main__":
    crear_base_datos()