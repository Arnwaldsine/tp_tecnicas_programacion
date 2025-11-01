import os
import re
import sqlite3
from typing import List, Tuple, Optional

from queries import gestion_queries as q

DB_PATH = "inventario.db"
PAGE_SIZE = 20  # mostrar 20 modelos por página en la sección de ventas/reposición

# ANSI color codes (funcionan en la mayoría de terminales)
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"
COLOR_BOLD = "\033[1m"

# Regex simple para tarjeta: acepta 16 dígitos, opcionalmente separados por espacios o guiones
CARD_REGEX = re.compile(r'^(?:\d{4}[- ]?){3}\d{4}$')


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def conectar_db():
    return sqlite3.connect(DB_PATH)


def mostrar_resultados(resultados: List[Tuple]):
    if resultados:
        print("\n--- RESULTADOS ---")
        for producto in resultados:
            print(
                f"ID: {producto[0]} | Modelo: {producto[1]} | Precio: ${producto[2]:.2f} | "
                f"Stock: {producto[3]} | Ventas: {producto[4]} | Marca: {producto[5]} | Tipo: {producto[6]}"
            )
    else:
        print("\nNo se encontraron productos")


def listar_tipos() -> List[Tuple[int, str]]:
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(q.SELECT_TODOS_TIPOS)
    rows = cur.fetchall()
    conn.close()
    return rows


def listar_marcas() -> List[Tuple[int, str]]:
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(q.SELECT_TODAS_MARCAS)
    rows = cur.fetchall()
    conn.close()
    return rows


def validar_tarjeta(tarjeta: str) -> bool:
    tarjeta = tarjeta.strip()
    return bool(CARD_REGEX.match(tarjeta))


def obtener_producto_por_modelo(modelo: str) -> Optional[Tuple]:
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(q.SELECT_MODELO_EXACTO, (modelo.lower(),))
    row = cur.fetchone()
    conn.close()
    return row


def seleccionar_producto_para_venta() -> Optional[Tuple[int, str, float, int]]:
    """
    Muestra páginas de productos con stock > 0 (PAGE_SIZE por página).
    Permite:
      - navegar con 'n' (siguiente) y 'p' (anterior),
      - buscar por nombre con 's',
      - seleccionar un producto escribiendo el número que aparece a la izquierda,
      - '0' para cancelar y volver.
    Devuelve una tupla con (id, modelo, precio, stock) del producto seleccionado,
    o None si el usuario cancela.
    """
    conn = conectar_db()
    cur = conn.cursor()
    page = 0

    while True:
        clear_screen()
        offset = page * PAGE_SIZE
        cur.execute(q.SELECT_PRODUCTOS_DISPONIBLES_PAGINATED, (PAGE_SIZE, offset))
        filas = cur.fetchall()

        if not filas and page > 0:
            # si no hay filas en esta página, retroceder una página (posible eliminado/consumo)
            page -= 1
            offset = page * PAGE_SIZE
            cur.execute(q.SELECT_PRODUCTOS_DISPONIBLES_PAGINATED, (PAGE_SIZE, offset))
            filas = cur.fetchall()

        print(f"--- SECCIÓN VENTAS: productos con stock (página {page + 1}) ---")
        if filas:
            for idx, fila in enumerate(filas, start=1):
                # fila: (id, modelo, precio, stock, ventas, marca, tipo)
                modelo = fila[1]
                precio = fila[2]
                stock = fila[3]
                marca = fila[5] or ""
                tipo = fila[6] or ""
                print(f"{idx}. {modelo} | ${precio:.2f} | Stock: {stock} | Marca: {marca} | Tipo: {tipo}")
        else:
            print("No hay productos con stock disponible.")

        print("\nOpciones:")
        print("  [n] Siguiente página")
        print("  [p] Página anterior")
        print("  [s] Buscar por nombre")
        print("  [0] Cancelar y volver")
        print("  [Número] Seleccionar producto por número de la página (ej. 1)")

        opcion = input("\nSeleccione opción: ").strip().lower()

        if opcion == "n":
            # intentar siguiente página
            cur.execute(q.SELECT_PRODUCTOS_DISPONIBLES_PAGINATED, (PAGE_SIZE, (page + 1) * PAGE_SIZE))
            next_page = cur.fetchall()
            if next_page:
                page += 1
            else:
                print("No hay más páginas.")
                input("Presione Enter para continuar...")
            continue
        elif opcion == "p":
            if page > 0:
                page -= 1
            else:
                print("Ya estás en la primera página.")
                input("Presione Enter para continuar...")
            continue
        elif opcion == "s":
            termino = input("Ingrese (parte de) modelo a buscar: ").strip().lower()
            if termino == "":
                print("Búsqueda vacía.")
                input("Presione Enter para continuar...")
                continue
            # limitar la búsqueda a un número razonable (ej. 200)
            cur.execute(q.SELECT_PRODUCTOS_DISPONIBLES_BUSCAR, (f"%{termino}%", 200))
            resultados_busqueda = cur.fetchall()
            clear_screen()
            print(f"--- RESULTADOS DE BÚSQUEDA para '{termino}' (productos con stock) ---")
            if not resultados_busqueda:
                print("No se encontraron coincidencias.")
                input("Presione Enter para continuar...")
                continue
            for idx, fila in enumerate(resultados_busqueda, start=1):
                print(f"{idx}. {fila[1]} | ${fila[2]:.2f} | Stock: {fila[3]} | Marca: {fila[5]} | Tipo: {fila[6]}")
            sel = input("\nIngrese número para seleccionar producto, o Enter para volver: ").strip()
            if sel == "":
                continue
            try:
                sel_i = int(sel)
                if 1 <= sel_i <= len(resultados_busqueda):
                    fila = resultados_busqueda[sel_i - 1]
                    conn.close()
                    return (fila[0], fila[1], fila[2], fila[3])
                else:
                    print("Número fuera de rango.")
                    input("Presione Enter para continuar...")
                    continue
            except ValueError:
                print("Entrada inválida.")
                input("Presione Enter para continuar...")
                continue
        elif opcion == "0":
            conn.close()
            return None
        else:
            # intentar interpretar como número de la página actual
            try:
                elegido = int(opcion)
                if 1 <= elegido <= len(filas):
                    fila = filas[elegido - 1]
                    conn.close()
                    return (fila[0], fila[1], fila[2], fila[3])
                else:
                    print("Número fuera de rango en la página.")
                    input("Presione Enter para continuar...")
                    continue
            except ValueError:
                print("Opción no reconocida.")
                input("Presione Enter para continuar...")
                continue


def seleccionar_producto_para_reponer() -> Optional[Tuple[int, str, float, int]]:
    """
    Similar a seleccionar_producto_para_venta, pero lista todos los productos
    independientemente del stock (útil para reposición).
    Permite paginar, buscar y seleccionar.
    Devuelve (id, modelo, precio, stock) o None.
    """
    conn = conectar_db()
    cur = conn.cursor()
    page = 0

    # SQL paginado sin filtrar por stock
    SELECT_PRODUCTOS_PAGINATED_ALL = """
    SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
    FROM productos p
    LEFT JOIN marcas m ON p.marca_id = m.id
    LEFT JOIN tipos_producto t ON p.tipo_id = t.id
    ORDER BY LOWER(p.modelo)
    LIMIT ? OFFSET ?
    """

    SELECT_PRODUCTOS_BUSCAR_ALL = """
    SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
    FROM productos p
    LEFT JOIN marcas m ON p.marca_id = m.id
    LEFT JOIN tipos_producto t ON p.tipo_id = t.id
    WHERE LOWER(p.modelo) LIKE ?
    ORDER BY LOWER(p.modelo)
    LIMIT ?
    """

    while True:
        clear_screen()
        offset = page * PAGE_SIZE
        cur.execute(SELECT_PRODUCTOS_PAGINATED_ALL, (PAGE_SIZE, offset))
        filas = cur.fetchall()

        if not filas and page > 0:
            page -= 1
            offset = page * PAGE_SIZE
            cur.execute(SELECT_PRODUCTOS_PAGINATED_ALL, (PAGE_SIZE, offset))
            filas = cur.fetchall()

        print(f"--- REPONER: productos (página {page + 1}) ---")
        if filas:
            for idx, fila in enumerate(filas, start=1):
                modelo = fila[1]
                precio = fila[2]
                stock = fila[3]
                marca = fila[5] or ""
                tipo = fila[6] or ""
                print(f"{idx}. {modelo} | ${precio:.2f} | Stock: {stock} | Marca: {marca} | Tipo: {tipo}")
        else:
            print("No hay productos en la base de datos.")

        print("\nOpciones:")
        print("  [n] Siguiente página")
        print("  [p] Página anterior")
        print("  [s] Buscar por nombre")
        print("  [0] Cancelar y volver")
        print("  [Número] Seleccionar producto por número de la página (ej. 1)")

        opcion = input("\nSeleccione opción: ").strip().lower()

        if opcion == "n":
            cur.execute(SELECT_PRODUCTOS_PAGINATED_ALL, (PAGE_SIZE, (page + 1) * PAGE_SIZE))
            next_page = cur.fetchall()
            if next_page:
                page += 1
            else:
                print("No hay más páginas.")
                input("Presione Enter para continuar...")
            continue
        elif opcion == "p":
            if page > 0:
                page -= 1
            else:
                print("Ya estás en la primera página.")
                input("Presione Enter para continuar...")
            continue
        elif opcion == "s":
            termino = input("Ingrese (parte de) modelo a buscar: ").strip().lower()
            if termino == "":
                print("Búsqueda vacía.")
                input("Presione Enter para continuar...")
                continue
            cur.execute(SELECT_PRODUCTOS_BUSCAR_ALL, (f"%{termino}%", 200))
            resultados_busqueda = cur.fetchall()
            clear_screen()
            print(f"--- RESULTADOS DE BÚSQUEDA para '{termino}' ---")
            if not resultados_busqueda:
                print("No se encontraron coincidencias.")
                input("Presione Enter para continuar...")
                continue
            for idx, fila in enumerate(resultados_busqueda, start=1):
                print(f"{idx}. {fila[1]} | ${fila[2]:.2f} | Stock: {fila[3]} | Marca: {fila[5]} | Tipo: {fila[6]}")
            sel = input("\nIngrese número para seleccionar producto, o Enter para volver: ").strip()
            if sel == "":
                continue
            try:
                sel_i = int(sel)
                if 1 <= sel_i <= len(resultados_busqueda):
                    fila = resultados_busqueda[sel_i - 1]
                    conn.close()
                    return (fila[0], fila[1], fila[2], fila[3])
                else:
                    print("Número fuera de rango.")
                    input("Presione Enter para continuar...")
                    continue
            except ValueError:
                print("Entrada inválida.")
                input("Presione Enter para continuar...")
                continue
        elif opcion == "0":
            conn.close()
            return None
        else:
            try:
                elegido = int(opcion)
                if 1 <= elegido <= len(filas):
                    fila = filas[elegido - 1]
                    conn.close()
                    return (fila[0], fila[1], fila[2], fila[3])
                else:
                    print("Número fuera de rango en la página.")
                    input("Presione Enter para continuar...")
                    continue
            except ValueError:
                print("Opción no reconocida.")
                input("Presione Enter para continuar...")
                continue