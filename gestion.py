import sqlite3

def conectar_db():
    """Conecta con la base de datos"""
    return sqlite3.connect('inventario.db')

def buscar_producto():
    """Opción 1: Buscar producto"""
    while True:
        print("\n--- BUSCAR PRODUCTO ---")
        print("1. Por Tipo")
        print("2. Por Marca")
        print("3. Por Modelo")
        print("4. Volver")
        
        opcion = input("\nSeleccione opción: ")
        
        if opcion == "1":
            buscar_por_tipo()
        elif opcion == "2":
            buscar_por_marca()
        elif opcion == "3":
            buscar_por_modelo()
        elif opcion == "4":
            break
        else:
            print("Opción inválida")

def buscar_por_tipo():
    """Buscar productos por tipo"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("\nTipos disponibles: Notebook, Celular, Reloj")
    tipo = input("Ingrese tipo: ").strip()
    
    cursor.execute("""
        SELECT nombre, precio, stock, ventas 
        FROM productos 
        WHERE nombre LIKE ?
    """, (f"%{tipo[0].lower()}%",))
    
    resultados = cursor.fetchall()
    mostrar_resultados(resultados)
    conn.close()

def buscar_por_marca():
    """Buscar productos por marca"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("\nMarcas: Dell, Asus, HP, Motorola, Samsung, Xiaomi, Casio")
    marca = input("Ingrese marca: ").strip().lower()
    
    cursor.execute("""
        SELECT nombre, precio, stock, ventas 
        FROM productos 
        WHERE nombre LIKE ?
    """, (f"%{marca[0]}%",))
    
    resultados = cursor.fetchall()
    mostrar_resultados(resultados)
    conn.close()

def buscar_por_modelo():
    """Buscar productos por modelo"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    modelo = input("Ingrese modelo: ").strip()
    
    cursor.execute("""
        SELECT nombre, precio, stock, ventas 
        FROM productos 
        WHERE nombre = ?
    """, (modelo,))
    
    resultados = cursor.fetchall()
    mostrar_resultados(resultados)
    conn.close()

def mostrar_resultados(resultados):
    """Muestra los resultados de búsqueda"""
    if resultados:
        print("\n--- RESULTADOS ---")
        for producto in resultados:
            print(f"Modelo: {producto[0]} | Precio: ${producto[1]} | Stock: {producto[2]} | Ventas: {producto[3]}")
    else:
        print("\nNo se encontraron productos")

def vender_producto():
    """Opción 2: Vender producto"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    while True:
        print("\n--- VENDER PRODUCTO ---")
        modelo = input("Ingrese modelo: ").strip()
        
        # Verificar si existe el producto
        cursor.execute("SELECT nombre, precio, stock FROM productos WHERE nombre = ?", (modelo,))
        producto = cursor.fetchone()
        
        if not producto:
            print("Producto no encontrado")
            continue
        
        if producto[2] <= 0:
            print("Producto sin stock")
            continue
        
        cantidad = int(input("Ingrese cantidad: "))
        
        if cantidad > producto[2]:
            print(f"Stock insuficiente. Disponible: {producto[2]}")
            continue
        
        total = producto[1] * cantidad
        print(f"\nTotal a pagar: ${total}")
        
        # Simulación de pago
        while True:
            print("\n--- PAGO ---")
            tarjeta = input("Ingrese su tarjeta de crédito (16 dígitos): ")
            
            print("\n0. Ingresar otra tarjeta")
            print("1. Terminar pago")
            print("2. Volver")
            
            opcion = input("\nSeleccione opción: ")
            
            if opcion == "1":
                # Actualizar stock y ventas
                cursor.execute("""
                    UPDATE productos 
                    SET stock = stock - ?, ventas = ventas + ? 
                    WHERE nombre = ?
                """, (cantidad, cantidad, modelo))
                conn.commit()
                print("\n¡Venta realizada con éxito!")
                conn.close()
                return
            elif opcion == "2":
                conn.close()
                return
            elif opcion == "0":
                continue
            else:
                print("Opción inválida")

def reponer_producto():
    """Opción 3: Reponer producto"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    while True:
        print("\n--- REPONER PRODUCTO ---")
        modelo = input("Ingrese modelo: ").strip()
        
        cursor.execute("SELECT nombre, stock FROM productos WHERE nombre = ?", (modelo,))
        producto = cursor.fetchone()
        
        if not producto:
            print("Producto no encontrado")
            continue
        
        print(f"Stock actual: {producto[1]}")
        cantidad = int(input("Ingrese cantidad a reponer: "))
        
        print("\n1. Cantidad equivocada")
        print("0. Confirmar y volver")
        
        opcion = input("\nSeleccione opción: ")
        
        if opcion == "0":
            cursor.execute("""
                UPDATE productos 
                SET stock = stock + ? 
                WHERE nombre = ?
            """, (cantidad, modelo))
            conn.commit()
            print("\n¡Reposición exitosa!")
            conn.close()
            return
        elif opcion == "1":
            continue
        else:
            print("Opción inválida")

def productos_mas_vendidos():
    """Opción 4: Productos más vendidos"""
    conn = conectar_db()
    cursor = conn.cursor()
    
    print("\n--- PRODUCTOS MÁS VENDIDOS ---")
    
    cursor.execute("""
        SELECT nombre, ventas 
        FROM productos 
        ORDER BY ventas DESC
    """)
    
    resultados = cursor.fetchall()
    
    for i, producto in enumerate(resultados, 1):
        print(f"{i}. Modelo: {producto[0]} | Cantidad vendida: {producto[1]}")
    
    input("\n0. Volver (Presione Enter)")
    conn.close()

def menu_principal():
    """Menú principal del sistema"""
    while True:
        print("\n" + "="*40)
        print("SISTEMA DE GESTIÓN DE PRODUCTOS")
        print("="*40)
        print("1. Buscar producto")
        print("2. Vender producto")
        print("3. Reponer producto")
        print("4. Productos más vendidos")
        print("5. Salir")
        
        opcion = input("\nSeleccione opción: ")
        
        if opcion == "1":
            buscar_producto()
        elif opcion == "2":
            vender_producto()
        elif opcion == "3":
            reponer_producto()
        elif opcion == "4":
            productos_mas_vendidos()
        elif opcion == "5":
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu_principal()