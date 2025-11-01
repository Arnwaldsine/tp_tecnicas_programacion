from queries import gestion_queries as q
from helpers import (
    clear_screen,
    conectar_db,
    mostrar_resultados,
    listar_tipos,
    listar_marcas,
    validar_tarjeta,
    seleccionar_producto_para_venta,
    seleccionar_producto_para_reponer,
    COLOR_RESET,
    COLOR_GREEN,
    COLOR_BOLD
)


def buscar_por_tipo() -> bool:
    """
    Buscar productos por tipo usando la tabla tipos_producto.
    Retorna True si el usuario eligió volver al menú principal (opción 0).
    """
    while True:
        clear_screen()
        tipos = listar_tipos()
        if not tipos:
            print("No hay tipos disponibles en la base de datos.")
            input("Presione Enter para volver...")
            return False

        print("\nTipos disponibles:")
        for tid, nombre in tipos:
            print(f"{tid}. {nombre}")

        print("0. Volver al menú principal")
        entrada = input("Ingrese ID o nombre del tipo (o 0 para volver): ").strip()
        if entrada == "0":
            return True

        tipo_id = None
        # intentar por ID
        if entrada.isdigit():
            tipo_id = int(entrada)
        else:
            # buscar por nombre (case-insensitive)
            for tid, nombre in tipos:
                if nombre.lower() == entrada.lower():
                    tipo_id = tid
                    break

        if tipo_id is None:
            print("Tipo no encontrado.")
            input("Presione Enter para volver...")
            return False

        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(q.SELECT_POR_TIPO, (tipo_id,))
        resultados = cur.fetchall()
        conn.close()
        mostrar_resultados(resultados)
        input("\nPresione Enter para volver...")
        return False


def buscar_por_marca() -> bool:
    """
    Buscar productos por marca usando la tabla marcas.
    Retorna True si el usuario eligió volver al menú principal (opción 0).
    """
    while True:
        clear_screen()
        marcas = listar_marcas()
        if not marcas:
            print("No hay marcas disponibles en la base de datos.")
            input("Presione Enter para volver...")
            return False

        print("\nMarcas disponibles:")
        for mid, nombre in marcas:
            print(f"{mid}. {nombre}")

        print("0. Volver al menú principal")
        entrada = input("Ingrese ID o nombre de la marca (o 0 para volver): ").strip()
        if entrada == "0":
            return True

        marca_id = None
        if entrada.isdigit():
            marca_id = int(entrada)
        else:
            for mid, nombre in marcas:
                if nombre.lower() == entrada.lower():
                    marca_id = mid
                    break

        if marca_id is None:
            print("Marca no encontrada.")
            input("Presione Enter para volver...")
            return False

        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(q.SELECT_POR_MARCA, (marca_id,))
        resultados = cur.fetchall()
        conn.close()
        mostrar_resultados(resultados)
        input("\nPresione Enter para volver...")
        return False


def buscar_por_modelo() -> bool:
    """
    Buscar productos por modelo (coincidencia parcial).
    Retorna True si el usuario eligió volver al menú principal (opción 0).
    """
    while True:
        clear_screen()
        print("0. Volver al menú principal")
        entrada = input("Ingrese (parte de) modelo (o 0 para volver): ").strip()
        if entrada == "0":
            return True

        if not entrada:
            print("Modelo vacío.")
            input("Presione Enter para volver...")
            return False

        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(q.SELECT_POR_MODELO_LIKE, (f"%{entrada.lower()}%",))
        resultados = cur.fetchall()
        conn.close()
        mostrar_resultados(resultados)
        input("\nPresione Enter para volver...")
        return False


def buscar_producto():
    """
    Submenú de búsqueda.
    """
    while True:
        clear_screen()
        print("\n--- BUSCAR PRODUCTO ---")
        print("0. Volver al menú principal")
        print("1. Por Tipo")
        print("2. Por Marca")
        print("3. Por Modelo")

        opcion = input("\nSeleccione opción: ").strip()

        if opcion == "0":
            return  # vuelve al menú principal
        if opcion == "1":
            if buscar_por_tipo():
                return
        elif opcion == "2":
            if buscar_por_marca():
                return
        elif opcion == "3":
            if buscar_por_modelo():
                return
        else:
            print("Opción inválida")
            input("Presione Enter para continuar...")


def vender_producto():
    """
    Flujo de venta actualizado con opción de cancelar en cualquier momento.
    """
    seleccionado = seleccionar_producto_para_venta()
    if seleccionado is None:
        return  # el usuario canceló y volvió al menú principal

    prod_id, prod_modelo, prod_precio, prod_stock = seleccionado

    conn = conectar_db()
    cursor = conn.cursor()

    if prod_stock <= 0:
        print("Producto sin stock")
        input("Presione Enter para volver...")
        conn.close()
        return

    # Solicitar cantidad
    while True:
        clear_screen()
        print("\n--- VENTA DE PRODUCTO ---")
        print(f"Producto: {prod_modelo}")
        print(f"Precio: ${prod_precio:.2f}")
        print(f"Stock disponible: {prod_stock}")
        print("\n0. Cancelar y volver al menú principal")
        
        cantidad_input = input("\nIngrese cantidad a vender: ").strip()
        
        if cantidad_input == "0":
            print("\nVenta cancelada.")
            input("Presione Enter para continuar...")
            conn.close()
            return
        
        try:
            cantidad = int(cantidad_input)
        except ValueError:
            print("Cantidad inválida")
            input("Presione Enter para continuar...")
            continue

        if cantidad <= 0:
            print("Cantidad debe ser mayor a 0")
            input("Presione Enter para continuar...")
            continue

        if cantidad > prod_stock:
            print(f"Stock insuficiente. Disponible: {prod_stock}")
            input("Presione Enter para continuar...")
            continue

        # Cantidad válida, proceder al pago
        total = prod_precio * cantidad
        
        # Proceso de pago
        while True:
            clear_screen()
            print("\n--- CONFIRMACIÓN DE VENTA ---")
            print(f"Producto: {prod_modelo}")
            print(f"Cantidad: {cantidad}")
            print(f"Total a pagar: ${total:.2f}")
            print("\n--- PAGO ---")
            print("0. Cancelar venta y volver")
            
            tarjeta = input("\nIngrese su tarjeta de crédito (16 dígitos, puede incluir espacios o guiones): ").strip()
            
            if tarjeta == "0":
                print("\nVenta cancelada.")
                input("Presione Enter para continuar...")
                conn.close()
                return
            
            if not validar_tarjeta(tarjeta):
                print("Formato de tarjeta inválido. Ejemplo válido: 1234 5678 9012 3456")
                print("\n1. Reingresar tarjeta")
                print("0. Cancelar venta")
                opcion = input("\nSeleccione opción: ").strip()
                if opcion == "0":
                    print("\nVenta cancelada.")
                    input("Presione Enter para continuar...")
                    conn.close()
                    return
                else:
                    continue

            # Tarjeta válida, confirmar pago
            clear_screen()
            print("\n--- CONFIRMACIÓN FINAL ---")
            print(f"Producto: {prod_modelo}")
            print(f"Cantidad: {cantidad}")
            print(f"Total: ${total:.2f}")
            print(f"Tarjeta: ****-****-****-{tarjeta.replace(' ', '').replace('-', '')[-4:]}")
            print("\n1. Confirmar y procesar pago")
            print("2. Cambiar tarjeta")
            print("0. Cancelar venta")

            opcion = input("\nSeleccione opción: ").strip()

            if opcion == "1":
                try:
                    cursor.execute(q.UPDATE_RESTAR_STOCK_Y_SUMAR_VENTAS, (cantidad, cantidad, prod_id))
                    conn.commit()
                    clear_screen()
                    print("\n" + "=" * 40)
                    print("¡VENTA REALIZADA CON ÉXITO!")
                    print("=" * 40)
                    print(f"Producto: {prod_modelo}")
                    print(f"Cantidad: {cantidad}")
                    print(f"Total pagado: ${total:.2f}")
                    print("=" * 40)
                except Exception as e:
                    conn.rollback()
                    print("\nOcurrió un error al procesar la venta:", e)
                finally:
                    conn.close()
                input("\nPresione Enter para continuar...")
                return
            elif opcion == "0":
                print("\nVenta cancelada.")
                input("Presione Enter para continuar...")
                conn.close()
                return
            elif opcion == "2":
                continue
            else:
                print("Opción inválida")
                input("Presione Enter para continuar...")


def reponer_producto():
    """
    Flujo de reposición con opción de cancelar en cualquier momento.
    """
    seleccionado = seleccionar_producto_para_reponer()
    if seleccionado is None:
        return  # usuario canceló

    prod_id, prod_modelo, prod_precio, prod_stock = seleccionado

    conn = conectar_db()
    cursor = conn.cursor()

    # Solicitar cantidad a reponer
    while True:
        clear_screen()
        print("\n--- REPOSICIÓN DE STOCK ---")
        print(f"Producto: {prod_modelo}")
        print(f"Precio: ${prod_precio:.2f}")
        print(f"Stock actual: {prod_stock}")
        print("\n0. Cancelar y volver al menú principal")
        
        cantidad_input = input("\nIngrese cantidad a reponer: ").strip()
        
        if cantidad_input == "0":
            print("\nReposición cancelada.")
            input("Presione Enter para continuar...")
            conn.close()
            return
        
        try:
            cantidad = int(cantidad_input)
        except ValueError:
            print("Cantidad inválida")
            input("Presione Enter para continuar...")
            continue

        if cantidad <= 0:
            print("Cantidad debe ser mayor a 0")
            input("Presione Enter para continuar...")
            continue

        # Cantidad válida, mostrar confirmación
        nuevo_stock = prod_stock + cantidad
        clear_screen()
        print("\n--- CONFIRMACIÓN DE REPOSICIÓN ---")
        print(f"Producto: {prod_modelo}")
        print(f"Stock actual: {prod_stock}")
        print(f"Cantidad a reponer: {cantidad}")
        print(f"Stock después de reposición: {nuevo_stock}")
        print("\n1. Confirmar reposición")
        print("2. Cambiar cantidad")
        print("0. Cancelar reposición")

        opcion = input("\nSeleccione opción: ").strip()

        if opcion == "1":
            try:
                cursor.execute(q.UPDATE_SUMAR_STOCK, (cantidad, prod_id))
                conn.commit()
                clear_screen()
                print("\n" + "=" * 40)
                print("¡REPOSICIÓN EXITOSA!")
                print("=" * 40)
                print(f"Producto: {prod_modelo}")
                print(f"Cantidad repuesta: {cantidad}")
                print(f"Stock anterior: {prod_stock}")
                print(f"Stock nuevo: {nuevo_stock}")
                print("=" * 40)
            except Exception as e:
                conn.rollback()
                print("\nOcurrió un error al reponer:", e)
            finally:
                conn.close()
            input("\nPresione Enter para continuar...")
            return
        elif opcion == "0":
            print("\nReposición cancelada.")
            input("Presione Enter para continuar...")
            conn.close()
            return
        elif opcion == "2":
            continue
        else:
            print("Opción inválida")
            input("Presione Enter para continuar...")


def productos_mas_vendidos():
    """
    Muestra los productos ordenados por ventas desc.
    Si la cantidad vendida (ventas) es > 0 se muestra en color verde (resaltado),
    si es 0 se muestra en color por defecto.
    """
    clear_screen()
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(q.SELECT_MAS_VENDIDOS)
    resultados = cur.fetchall()

    print("\n--- PRODUCTOS MÁS VENDIDOS ---\n")
    if not resultados:
        print("No hay productos para mostrar.")
        input("\nPresione Enter para volver...")
        conn.close()
        return

    for i, producto in enumerate(resultados, 1):
        modelo = producto[1]
        ventas = producto[4]
        marca = producto[5] or ""
        tipo = producto[6] or ""
        # Si ventas > 0 mostramos el texto de la línea en verde; si no, normal.
        if ventas > 0:
            line = (
                f"{COLOR_GREEN}{i}. Modelo: {modelo} | Marca: {marca} | Tipo: {tipo} | "
                f"{COLOR_BOLD}Cantidad vendida: {ventas}{COLOR_RESET}"
            )
        else:
            line = f"{i}. Modelo: {modelo} | Marca: {marca} | Tipo: {tipo} | Cantidad vendida: {ventas}"
        print(line)

    input("\n0. Volver (Presione Enter)")
    conn.close()


def menu_principal():
    while True:
        clear_screen()
        print("\n" + "=" * 40)
        print("SISTEMA DE GESTIÓN DE PRODUCTOS")
        print("=" * 40)
        print("1. Buscar producto")
        print("2. Vender producto")
        print("3. Reponer producto")
        print("4. Productos más vendidos")
        print("5. Salir")

        opcion = input("\nSeleccione opción: ").strip()

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
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    menu_principal()