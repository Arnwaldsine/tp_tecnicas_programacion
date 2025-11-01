import sqlite3
from queries import crear_base_queries as q

DB_PATH = "inventario.db"


def crear_base_datos():
    """
    Crea la base de datos usando las queries definidas en queries/crear_base_queries.py
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear tablas
    cursor.execute(q.CREATE_MARCAS_TABLE)
    cursor.execute(q.CREATE_TIPOS_TABLE)
    cursor.execute(q.CREATE_PRODUCTOS_TABLE)
    print("Tablas 'marcas', 'tipos_producto' y 'productos' creadas (marca_id y tipo_id = NOT NULL)")

    # Insertar marcas y tipos iniciales
    cursor.executemany(q.INSERT_MARCA, q.MARCAS_INICIALES)
    cursor.executemany(q.INSERT_TIPO, q.TIPOS_INICIALES)

    # Recuperar diccionarios nombre->id
    cursor.execute('SELECT id, nombre FROM marcas')
    marcas_db = {nombre: mid for (mid, nombre) in cursor.fetchall()}

    cursor.execute('SELECT id, nombre FROM tipos_producto')
    tipos_db = {nombre: tid for (tid, nombre) in cursor.fetchall()}

    # Mapear marca/tipo por palabras clave (misma lógica que antes)
    modelo_a_marca = {
        'Inspiron': 'Dell', 'XPS': 'Dell', 'Latitude': 'Dell',
        'ZenBook': 'Asus', 'VivoBook': 'Asus', 'ROG': 'Asus',
        'Pavilion': 'HP', 'Envy': 'HP', 'Spectre': 'HP',
        'Moto': 'Motorola', 'Galaxy': 'Samsung', 'Redmi': 'Xiaomi',
        'Xiaomi': 'Xiaomi', 'Mi Band': 'Xiaomi', 'Mi Watch': 'Xiaomi',
        'G-Shock': 'Casio', 'Casio': 'Casio', 'Edifice': 'Casio',
    }

    modelo_a_tipo = {
        'Inspiron': 'Notebook', 'XPS': 'Notebook', 'Latitude': 'Notebook',
        'ZenBook': 'Notebook', 'VivoBook': 'Notebook', 'ROG': 'Notebook',
        'Pavilion': 'Notebook', 'Envy': 'Notebook', 'Spectre': 'Notebook',
        'Moto': 'Celular', 'Galaxy': 'Celular', 'Redmi': 'Celular',
        'Xiaomi': 'Celular', 'Mi Band': 'Reloj', 'Mi Watch': 'Reloj',
        'Redmi Watch': 'Reloj', 'G-Shock': 'Reloj', 'Casio': 'Reloj', 'Edifice': 'Reloj',
    }

    # Preparar productos con marca_id y tipo_id
    productos_con_ids = []
    for modelo, precio, stock, ventas in q.PRODUCTOS_INICIALES:
        marca_nombre = None
        tipo_nombre = None
        for clave, marca in modelo_a_marca.items():
            if clave in modelo:
                marca_nombre = marca
                break
        for clave, tipo in modelo_a_tipo.items():
            if clave in modelo:
                tipo_nombre = tipo
                break

        if marca_nombre is None or tipo_nombre is None:
            print(f"Advertencia: no se pudo determinar marca/tipo para '{modelo}', se omite.")
            continue

        marca_id = marcas_db.get(marca_nombre)
        tipo_id = tipos_db.get(tipo_nombre)

        if marca_id is None or tipo_id is None:
            print(f"Advertencia: falta id de marca o tipo para '{modelo}', se omite.")
            continue

        productos_con_ids.append((modelo, precio, stock, ventas, marca_id, tipo_id))

    # Insertar productos
    cursor.executemany(q.INSERT_PRODUCTO, productos_con_ids)
    conn.commit()
    print(f"Se intentaron insertar {len(q.PRODUCTOS_INICIALES)} productos de ejemplo (insertados: {len(productos_con_ids)})")

    # Mostrar resumen opcional
    cursor.execute("SELECT * FROM marcas")
    marcas = cursor.fetchall()
    print("\n--- MARCAS EN LA BASE DE DATOS ---")
    for m in marcas:
        print(f"{m[0]:<5} {m[1]:<15} {m[2] or ''}")

    cursor.execute("SELECT * FROM tipos_producto")
    tipos = cursor.fetchall()
    print("\n--- TIPOS DE PRODUCTO EN LA BASE DE DATOS ---")
    for t in tipos:
        print(f"{t[0]:<5} {t[1]:<15} {t[2] or ''}")

    cursor.execute(q.SELECT_ALL_PRODUCTS_WITH_JOIN if hasattr(q, 'SELECT_ALL_PRODUCTS_WITH_JOIN') else """
        SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
        FROM productos p
        LEFT JOIN marcas m ON p.marca_id = m.id
        LEFT JOIN tipos_producto t ON p.tipo_id = t.id
        ORDER BY p.id
    """)
    productos = cursor.fetchall()
    print("\n--- PRODUCTOS EN LA BASE DE DATOS ---")
    for p in productos:
        marca = p[5] if p[5] is not None else 'N/A'
        tipo = p[6] if p[6] is not None else 'N/A'
        print(f"{p[0]:<5} {p[1]:<25} ${p[2]:<9.2f} {p[3]:<8} {p[4]:<8} {marca:<12} {tipo}")

    conn.close()
    print("\n¡Base de datos creada y poblada exitosamente!")


if __name__ == "__main__":
    crear_base_datos()