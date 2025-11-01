# Sistema de Gestión de Inventario de Productos

## 📋 Descripción

Sistema de Gestión de Inventario desarrollado en Python con arquitectura modular que permite administrar productos electrónicos (notebooks, celulares y relojes) mediante una base de datos SQLite relacional. El sistema cuenta con una interfaz de consola mejorada, paginación de resultados, búsqueda avanzada y validaciones completas.

## 🗂️ Estructura del Proyecto

```
tp_tecnicas_programacion/
│
├── gestion.py                      # Módulo principal - Lógica de negocio y flujos
├── helpers.py                      # Funciones auxiliares y utilidades
├── crear_base.py                   # Script de inicialización de la BD
├── inventario.db                   # Base de datos SQLite (generada)
│
├── queries/                        # Módulo de consultas SQL
│   ├── gestion_queries.py         # Queries para operaciones de gestión
│   └── crear_base_queries.py      # Queries para creación de BD
│
└── README.md                       # Este archivo
```

## 🏗️ Arquitectura del Sistema

### Separación de Responsabilidades

- **gestion.py**: Contiene la lógica de negocio y los flujos principales del sistema
- **helpers.py**: Funciones de utilidad (conexión DB, validaciones, paginación, interfaz)
- **queries/**: Módulo separado con todas las consultas SQL organizadas por funcionalidad
- **crear_base.py**: Script independiente para inicializar la base de datos

### Base de Datos Relacional

El sistema utiliza un modelo relacional normalizado con tres tablas:

```
┌─────────────┐         ┌──────────────┐         ┌────────────────┐
│   marcas    │         │  productos   │         │ tipos_producto │
├─────────────┤         ├──────────────┤         ├────────────────┤
│ id (PK)     │◄────────│ marca_id(FK) │         │ id (PK)        │
│ nombre      │         │ tipo_id (FK) │────────►│ nombre         │
│ descripcion │         │ modelo       │         │ descripcion    │
└─────────────┘         │ precio       │         └────────────────┘
                        │ stock        │
                        │ ventas       │
                        └──────────────┘
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.x instalado
- Módulo `sqlite3` (incluido por defecto en Python)

### Paso 1: Crear la Base de Datos

```bash
python crear_base.py
```

Este script:
- ✅ Crea las tablas `marcas`, `tipos_producto` y `productos`
- ✅ Establece relaciones de integridad referencial (Foreign Keys)
- ✅ Inserta datos iniciales de marcas: Dell, Asus, HP, Motorola, Samsung, Xiaomi, Casio
- ✅ Inserta tipos de producto: Notebook, Celular, Reloj
- ✅ Carga productos de ejemplo con sus relaciones

### Paso 2: Ejecutar el Sistema

```bash
python gestion.py
```

## 📖 Documentación Detallada de Flujos

### Menú Principal

```
========================================
SISTEMA DE GESTIÓN DE PRODUCTOS
========================================
1. Buscar producto
2. Vender producto
3. Reponer producto
4. Productos más vendidos
5. Salir
```

---

## 1️⃣ FLUJO: Buscar Producto

### Descripción
Permite buscar productos utilizando tres métodos diferentes con el modelo relacional actualizado.

### Flujo General

```
INICIO (Opción 1 del Menú Principal)
    ↓
┌──────────────────────────────────┐
│   MENÚ BUSCAR PRODUCTO           │
│   0. Volver al menú principal    │
│   1. Por Tipo                    │
│   2. Por Marca                   │
│   3. Por Modelo                  │
└──────────────────────────────────┘
```

#### 1.1 Búsqueda por Tipo
**Función:** `buscar_por_tipo()`

**Flujo Detallado:**

```
Seleccionar opción "1"
    ↓
Sistema consulta tabla tipos_producto
    ↓
┌─────────────────────────────────────┐
│   TIPOS DISPONIBLES:                │
│   1. Notebook                       │
│   2. Celular                        │
│   3. Reloj                          │
│   0. Volver al menú principal       │
└─────────────────────────────────────┘
    ↓
Usuario puede ingresar:
  • ID del tipo (ej: 1)
  • Nombre del tipo (ej: "Notebook")
  • 0 para volver
    ↓
Sistema realiza JOIN:
  SELECT p.*, m.nombre, t.nombre
  FROM productos p
  JOIN marcas m ON p.marca_id = m.id
  JOIN tipos_producto t ON p.tipo_id = t.id
  WHERE p.tipo_id = ?
    ↓
Mostrar resultados con:
  • ID, Modelo, Precio, Stock, Ventas
  • Marca asociada
  • Tipo asociado
    ↓
Presionar Enter para volver
```

**Ejemplo de salida:**
```
--- RESULTADOS ---
ID: 1 | Modelo: Dell Inspiron 15 | Precio: $850.00 | Stock: 15 | Ventas: 0 | Marca: Dell | Tipo: Notebook
ID: 2 | Modelo: Dell XPS 13 | Precio: $920.00 | Stock: 10 | Ventas: 0 | Marca: Dell | Tipo: Notebook
```

#### 1.2 Búsqueda por Marca
**Función:** `buscar_por_marca()`

**Flujo Detallado:**

```
Seleccionar opción "2"
    ↓
Sistema consulta tabla marcas
    ↓
┌─────────────────────────────────────┐
│   MARCAS DISPONIBLES:               │
│   1. Dell                           │
│   2. Asus                           │
│   3. HP                             │
│   4. Motorola                       │
│   5. Samsung                        │
│   6. Xiaomi                         │
│   7. Casio                          │
│   0. Volver al menú principal       │
└─────────────────────────────────────┘
    ↓
Usuario puede ingresar:
  • ID de la marca (ej: 1)
  • Nombre de la marca (ej: "Samsung")
  • 0 para volver
    ↓
Sistema busca productos con marca_id = selección
    ↓
Mostrar resultados con JOIN
    ↓
Presionar Enter para volver
```

**Características:**
- ✅ Búsqueda insensible a mayúsculas/minúsculas
- ✅ Valida que la marca exista en la BD
- ✅ Muestra información completa con relaciones

#### 1.3 Búsqueda por Modelo
**Función:** `buscar_por_modelo()`

**Flujo Detallado:**

```
Seleccionar opción "3"
    ↓
┌────────────────────────────────────────────┐
│  0. Volver al menú principal               │
│  Ingrese (parte de) modelo: _____          │
└────────────────────────────────────────────┘
    ↓
Usuario ingresa texto (ej: "Galaxy")
    ↓
Sistema busca con LIKE:
  WHERE LOWER(p.modelo) LIKE '%galaxy%'
    ↓
Mostrar todos los productos que coincidan
    ↓
Presionar Enter para volver
```

**Características:**
- ✅ Búsqueda por coincidencia parcial
- ✅ No distingue mayúsculas/minúsculas
- ✅ Puede encontrar múltiples productos

---

## 2️⃣ FLUJO: Vender Producto

### Descripción
Proceso completo de venta con **interfaz paginada**, búsqueda integrada, validación de stock y pago con tarjeta.

### Flujo Detallado

```
INICIO (Opción 2 del Menú Principal)
    ↓
┌───────────────────────────────────────────────────────┐
│  SECCIÓN VENTAS: productos con stock (página 1)       │
│  1. Dell Inspiron 15 | $850.00 | Stock: 15 | Dell     │
│  2. Dell XPS 13 | $920.00 | Stock: 10 | Dell          │
│  3. Asus ZenBook | $780.00 | Stock: 12 | Asus         │
│  ...                                                  │
│  20. Producto... (máximo 20 por página)               │
│                                                       │
│  Opciones:                                            │
│  [n] Siguiente página                                 │
│  [p] Página anterior                                  │
│  [s] Buscar por nombre                                │
│  [0] Cancelar y volver                                │
│  [Número] Seleccionar producto (ej. 1)                │
└───────────────────────────────────────────────────────┘
    ↓
┌─── OPCIONES DEL USUARIO ────────┐
│                                 │
│ [n] → Siguiente página          │
│        ├─ Hay productos?        │
│        │   ├─ SÍ → Avanzar      │
│        │   └─ NO → Mensaje      │
│                                 │
│ [p] → Página anterior           │
│        ├─ Estás en página 1?    │
│        │   ├─ SÍ → Mensaje      │
│        │   └─ NO → Retroceder   │
│                                 │
│ [s] → BUSCAR POR NOMBRE         │
│        ↓                        │
│   Ingrese término: ____         │
│        ↓                        │
│   Sistema busca con LIKE        │
│   en productos con stock > 0    │
│        ↓                        │
│   Muestra hasta 200 resultados  │
│        ↓                        │
│   Usuario selecciona número     │
│        └─ Producto seleccionado │
│                                 │
│ [0] → Cancelar y volver         │
│                                 │
│ [1-20] → Seleccionar            │
│           producto de página    │
└─────────────────────────────────┘
    ↓
Producto seleccionado → (id, modelo, precio, stock)
    ↓
┌───────────────────────────────────────┐
│   VENTA DE PRODUCTO                   │
│   Producto: Dell Inspiron 15          │
│   Precio: $850.00                     │
│   Stock disponible: 15                │
│                                       │
│   0. Cancelar y volver al menú        │
│   Ingrese cantidad a vender: ___      │
└───────────────────────────────────────┘
    ↓
Validaciones:
  ├─ ¿Cantidad > 0? NO → Error, reintentar
  ├─ ¿Cantidad ≤ Stock? NO → "Stock insuficiente"
  └─ SÍ → Continuar
    ↓
Calcular total = precio × cantidad
    ↓
┌────────────────────────────────────────────┐
│   CONFIRMACIÓN DE VENTA                    │
│   Producto: Dell Inspiron 15               │
│   Cantidad: 2                              │
│   Total a pagar: $1700.00                  │
│                                            │
│   --- PAGO ---                             │
│   0. Cancelar venta y volver               │
│   Ingrese tarjeta (16 dígitos): ________   │
└────────────────────────────────────────────┘
    ↓
Validación de tarjeta con REGEX:
  ^(?:\d{4}[- ]?){3}\d{4}$
  Acepta: 1234567812345678
          1234-5678-9012-3456
          1234 5678 9012 3456
    ↓
  ¿Tarjeta válida?
  │
  ├─ NO → Mostrar error
  │        1. Reingresar tarjeta
  │        0. Cancelar venta
  │
  └─ SÍ → Mostrar confirmación final
           ↓
┌──────────────────────────────────────────┐
│   CONFIRMACIÓN FINAL                     │
│   Producto: Dell Inspiron 15             │
│   Cantidad: 2                            │
│   Total: $1700.00                        │
│   Tarjeta: ****-****-****-5678           │
│                                          │
│   1. Confirmar y procesar pago           │
│   2. Cambiar tarjeta                     │
│   0. Cancelar venta                      │
└──────────────────────────────────────────┘
    ↓
Usuario selecciona:
│
├─ Opción 1 → PROCESAR VENTA
│              ↓
│         UPDATE productos
│         SET stock = stock - cantidad,
│             ventas = ventas + cantidad
│         WHERE id = producto_id
│              ↓
│         COMMIT a la BD
│              ↓
│    ┌────────────────────────────────┐
│    │ ¡VENTA REALIZADA CON ÉXITO!    │
│    │ Producto: Dell Inspiron 15     │
│    │ Cantidad: 2                    │
│    │ Total pagado: $1700.00         │
│    └────────────────────────────────┘
│              ↓
│         Volver al menú principal
│
├─ Opción 2 → Volver a ingresar tarjeta
│
└─ Opción 0 → Cancelar venta y volver
```

### Función Principal
**Función:** `vender_producto()`  
**Helper:** `seleccionar_producto_para_venta()` en `helpers.py`

### Características Destacadas

✅ **Paginación Inteligente**: 20 productos por página  
✅ **Búsqueda Integrada**: Buscar sin salir del flujo de venta  
✅ **Solo Stock Disponible**: Filtra automáticamente productos con stock > 0  
✅ **Validación de Tarjeta**: Regex que acepta múltiples formatos  
✅ **Cancelación en Cualquier Momento**: Opción "0" siempre disponible  
✅ **Transacciones Seguras**: Rollback automático en caso de error  
✅ **Confirmación Doble**: Evita ventas accidentales  

---

## 3️⃣ FLUJO: Reponer Producto

### Descripción
Permite añadir stock a cualquier producto del inventario con interfaz paginada y búsqueda.

### Flujo Detallado

```
INICIO (Opción 3 del Menú Principal)
    ↓
┌──────────────────────────────────────────────────────┐
│  REPONER: productos (página 1)                       │
│  (TODOS LOS PRODUCTOS, incluso sin stock)            │
│                                                      │
│  1. Dell Inspiron 15 | $850.00 | Stock: 15 | Dell    │
│  2. Asus ZenBook | $780.00 | Stock: 0 | Asus         │
│  3. HP Pavilion | $800.00 | Stock: 5 | HP            │
│  ...                                                 │
│                                                      │
│  Opciones:                                           │
│  [n] Siguiente página                                │
│  [p] Página anterior                                 │
│  [s] Buscar por nombre                               │
│  [0] Cancelar y volver                               │
│  [Número] Seleccionar producto (ej. 2)               │
└──────────────────────────────────────────────────────┘
    ↓
Usuario navega/busca y selecciona producto
    ↓
Producto seleccionado → (id, modelo, precio, stock_actual)
    ↓
┌─────────────────────────────────────────┐
│   REPOSICIÓN DE STOCK                   │
│   Producto: Asus ZenBook                │
│   Precio: $780.00                       │
│   Stock actual: 0                       │
│                                         │
│   0. Cancelar y volver al menú          │
│   Ingrese cantidad a reponer: ___       │
└─────────────────────────────────────────┘
    ↓
Validación:
  ├─ ¿Cantidad > 0? NO → Error, reintentar
  └─ SÍ → Continuar
    ↓
Calcular nuevo_stock = stock_actual + cantidad
    ↓
┌─────────────────────────────────────────┐
│   CONFIRMACIÓN DE REPOSICIÓN            │
│   Producto: Asus ZenBook                │
│   Stock actual: 0                       │
│   Cantidad a reponer: 10                │
│   Stock después de reposición: 10       │
│                                         │
│   1. Confirmar reposición               │
│   2. Cambiar cantidad                   │
│   0. Cancelar reposición                │
└─────────────────────────────────────────┘
    ↓
Usuario selecciona:
│
├─ Opción 1 → CONFIRMAR REPOSICIÓN
│              ↓
│         UPDATE productos
│         SET stock = stock + cantidad
│         WHERE id = producto_id
│              ↓
│         COMMIT a la BD
│              ↓
│    ┌────────────────────────────────┐
│    │ ¡REPOSICIÓN EXITOSA!           │
│    │ Producto: Asus ZenBook         │
│    │ Cantidad repuesta: 10          │
│    │ Stock anterior: 0              │
│    │ Stock nuevo: 10                │
│    └────────────────────────────────┘
│              ↓
│         Volver al menú principal
│
├─ Opción 2 → Volver a ingresar cantidad
│
└─ Opción 0 → Cancelar y volver
```

### Función Principal
**Función:** `reponer_producto()`  
**Helper:** `seleccionar_producto_para_reponer()` en `helpers.py`

### Diferencias con Ventas

| Aspecto | Vender | Reponer |
|---------|--------|---------|
| Filtro de Stock | Solo stock > 0 | Todos los productos |
| Validación | Cantidad ≤ stock | Cantidad > 0 |
| Operación SQL | stock - cantidad | stock + cantidad |
| Casos de Uso | Productos disponibles | Incluye productos agotados |

---

## 4️⃣ FLUJO: Productos Más Vendidos

### Descripción
Muestra un ranking completo de productos ordenados por cantidad de ventas con resaltado en color.

### Flujo Detallado

```
INICIO (Opción 4 del Menú Principal)
    ↓
Sistema ejecuta query:
  SELECT p.id, p.modelo, p.precio, p.stock, 
         p.ventas, m.nombre, t.nombre
  FROM productos p
  LEFT JOIN marcas m ON p.marca_id = m.id
  LEFT JOIN tipos_producto t ON p.tipo_id = t.id
  ORDER BY p.ventas DESC
    ↓
┌────────────────────────────────────────────────┐
│   --- PRODUCTOS MÁS VENDIDOS ---               │
│                                                │
│  (Productos con ventas > 0 en VERDE)           │
│                                                │
│  1. Modelo: Galaxy S23 | Marca: Samsung |      │
│     Tipo: Celular | Cantidad vendida: 25       │
│                                                │
│  2. Modelo: Dell Inspiron 15 | Marca: Dell |   │
│     Tipo: Notebook | Cantidad vendida: 15      │
│                                                │
│  3. Modelo: Redmi Note 12 | Marca: Xiaomi |    │
│     Tipo: Celular | Cantidad vendida: 12       │
│                                                │
│  ...                                           │
│                                                │
│  15. Modelo: Casio G-Shock | Marca: Casio |    │
│      Tipo: Reloj | Cantidad vendida: 0         │
│                                                │
│  0. Volver (Presione Enter)                    │
└────────────────────────────────────────────────┘
    ↓
Usuario presiona Enter
    ↓
Volver al menú principal
```

### Función Principal
**Función:** `productos_mas_vendidos()`

### Características Visuales

```python
# Colores ANSI implementados en helpers.py
COLOR_GREEN = "\033[32m"    # Verde para productos vendidos
COLOR_BOLD = "\033[1m"      # Negrita para resaltar
COLOR_RESET = "\033[0m"     # Resetear formato
```

**Lógica de Colores:**
- ✅ **Ventas > 0**: Línea completa en VERDE con negrita en cantidad
- ⚪ **Ventas = 0**: Texto normal sin color

---

## 5️⃣ FLUJO: Salir del Sistema

```
INICIO (Opción 5 del Menú Principal)
    ↓
Mostrar mensaje: "¡Hasta luego!"
    ↓
break → Terminar ejecución
    ↓
FIN DEL PROGRAMA
```

---

## 🔧 Módulo Helpers (helpers.py)

### Funciones de Utilidad

#### `clear_screen()`
Limpia la pantalla de la consola (multiplataforma).

#### `conectar_db() -> sqlite3.Connection`
Establece conexión con `inventario.db`.

#### `mostrar_resultados(resultados: List[Tuple])`
Formatea y muestra resultados de búsquedas con JOIN.

#### `listar_tipos() -> List[Tuple[int, str]]`
Obtiene todos los tipos de producto de la BD.

#### `listar_marcas() -> List[Tuple[int, str]]`
Obtiene todas las marcas de la BD.

#### `validar_tarjeta(tarjeta: str) -> bool`
Valida formato de tarjeta de crédito con regex.
```python
CARD_REGEX = r'^(?:\d{4}[- ]?){3}\d{4}$'
```

#### `obtener_producto_por_modelo(modelo: str) -> Optional[Tuple]`
Busca producto por modelo exacto (case-insensitive).

#### `seleccionar_producto_para_venta() -> Optional[Tuple]`
**Interfaz paginada** para seleccionar productos con stock > 0.

**Características:**
- 📄 Paginación de 20 productos
- 🔍 Búsqueda integrada
- ⬅️➡️ Navegación con 'n' (next) y 'p' (previous)
- 🔢 Selección por número
- ❌ Cancelación con '0'

#### `seleccionar_producto_para_reponer() -> Optional[Tuple]`
Similar a `seleccionar_producto_para_venta()` pero **sin filtrar por stock**.

---

## 📊 Módulo Queries

### queries/gestion_queries.py

Contiene todas las consultas SQL para operaciones de gestión:

```python
# Búsquedas
SELECT_POR_TIPO = """SELECT p.id, p.modelo, ... WHERE p.tipo_id = ?"""
SELECT_POR_MARCA = """SELECT p.id, p.modelo, ... WHERE p.marca_id = ?"""
SELECT_POR_MODELO_LIKE = """... WHERE LOWER(p.modelo) LIKE ?"""

# Operaciones
UPDATE_RESTAR_STOCK_Y_SUMAR_VENTAS = """
    UPDATE productos 
    SET stock = stock - ?, ventas = ventas + ? 
    WHERE id = ?
"""

UPDATE_SUMAR_STOCK = """
    UPDATE productos 
    SET stock = stock + ? 
    WHERE id = ?
"""

# Listados
SELECT_TODOS_TIPOS = """SELECT id, nombre FROM tipos_producto"""
SELECT_TODAS_MARCAS = """SELECT id, nombre FROM marcas"""
SELECT_MAS_VENDIDOS = """... ORDER BY ventas DESC"""

# Paginación
SELECT_PRODUCTOS_DISPONIBLES_PAGINATED = """... LIMIT ? OFFSET ?"""
```

### queries/crear_base_queries.py

Define la estructura de la BD y datos iniciales:

```python
CREATE_MARCAS_TABLE = """CREATE TABLE IF NOT EXISTS marcas (...)"""
CREATE_TIPOS_TABLE = """CREATE TABLE IF NOT EXISTS tipos_producto (...)"""
CREATE_PRODUCTOS_TABLE = """CREATE TABLE IF NOT EXISTS productos (...)"""

MARCAS_INICIALES = [('Dell',), ('Asus',), ...]
TIPOS_INICIALES = [('Notebook',), ('Celular',), ('Reloj',)]
PRODUCTOS_INICIALES = [
    ('Dell Inspiron 15', 850.00, 15, 0),
    ...
]
```

---

## 🗃️ Esquema de Base de Datos

### Tabla: marcas

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria autoincremental |
| nombre | TEXT | Nombre de la marca (UNIQUE, NOT NULL) |
| descripcion | TEXT | Descripción opcional |

### Tabla: tipos_producto

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria autoincremental |
| nombre | TEXT | Tipo de producto (UNIQUE, NOT NULL) |
| descripcion | TEXT | Descripción opcional |

### Tabla: productos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria autoincremental |
| modelo | TEXT | Modelo del producto (UNIQUE, NOT NULL) |
| precio | REAL | Precio unitario (NOT NULL) |
| stock | INTEGER | Cantidad disponible (DEFAULT 0) |
| ventas | INTEGER | Total de unidades vendidas (DEFAULT 0) |
| marca_id | INTEGER | FK a marcas.id (NOT NULL) |
| tipo_id | INTEGER | FK a tipos_producto.id (NOT NULL) |

**Integridad Referencial:**
```sql
FOREIGN KEY (marca_id) REFERENCES marcas(id)
FOREIGN KEY (tipo_id) REFERENCES tipos_producto(id)
```

---

## 🎯 Casos de Uso Comunes

### Caso 1: Venta Rápida de Producto Específico

1. Ejecutar `python gestion.py`
2. Opción `2` (Vender producto)
3. Presionar `[s]` (Buscar)
4. Ingresar nombre del producto (ej: "Galaxy")
5. Seleccionar producto de los resultados
6. Ingresar cantidad
7. Ingresar tarjeta de crédito
8. Confirmar venta

### Caso 2: Reponer Stock de Producto Agotado

1. Opción `3` (Reponer producto)
2. Navegar o buscar producto con stock bajo
3. Seleccionar producto
4. Ingresar cantidad a reponer
5. Confirmar reposición

### Caso 3: Análisis de Ventas por Marca

1. Opción `1` (Buscar producto)
2. Opción `2` (Por Marca)
3. Seleccionar marca (ej: "Samsung")
4. Revisar columna "Ventas" de cada producto
5. Opción `4` del menú principal para ver ranking global

### Caso 4: Navegación en Inventario Grande

1. Opción `2` o `3` (Vender/Reponer)
2. Usar `[n]` y `[p]` para navegar páginas
3. Observar 20 productos por página
4. Usar `[s]` para búsqueda rápida si es necesario

---

## 🛡️ Validaciones y Manejo de Errores

### Validaciones Implementadas

✅ **Existencia de Producto**: Verifica antes de operar  
✅ **Stock Suficiente**: No permite vender más del disponible  
✅ **Cantidades Positivas**: Rechaza valores ≤ 0  
✅ **Formato de Tarjeta**: Regex para 16 dígitos  
✅ **IDs de Relaciones**: Valida marca_id y tipo_id existen  
✅ **Entrada de Usuario**: Maneja inputs inválidos sin crashear  

### Manejo de Errores

```python
try:
    cursor.execute(query, params)
    conn.commit()
except Exception as e:
    conn.rollback()  # Revertir cambios
    print(f"Error: {e}")
finally:
    conn.close()  # Siempre cerrar conexión
```

---

## 🎨 Características de Interfaz

### Colores y Formato

```python
COLOR_GREEN = "\033[32m"   # Productos vendidos
COLOR_YELLOW = "\033[33m"  # Advertencias
COLOR_RED = "\033[31m"     # Errores
COLOR_BOLD = "\033[1m"     # Resaltar
```

### Paginación

- **PAGE_SIZE**: 20 productos por página
- Navegación intuitiva con letras y números
- Indicador de página actual

### Limpieza de Pantalla

Automática al cambiar de menú para mejor UX:
```python
os.system("cls" if os.name == "nt" else "clear")
```

---

## 🚀 Mejoras Implementadas (vs. Versión Original)

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| Arquitectura | Monolítico | Modular (gestion, helpers, queries) |
| Base de Datos | 1 tabla | 3 tablas relacionales normalizadas |
| Búsqueda | Por letra | Por relaciones (JOINs) |
| Selección Producto | Input manual | Interfaz paginada + búsqueda |
| Validación Tarjeta | Básica | Regex completo con formatos |
| Interfaz | Texto simple | Colores ANSI + paginación |
| Cancelación | Limitada | En cualquier punto del flujo |
| Código SQL | Embebido | Módulo separado (queries/) |
| Stock en Ventas | Ver todos | Solo disponibles |

---

## 📝 Convenciones de Código

### Estilo Python
- ✅ PEP 8 compliant
- ✅ Type hints en funciones clave
- ✅ Docstrings descriptivos
- ✅ Nombres descriptivos de variables

### Consultas SQL
- ✅ MAYÚSCULAS para keywords SQL
- ✅ Parámetros con `?` (prepared statements)
- ✅ JOINs explícitos (LEFT JOIN)
- ✅ Queries documentadas

---

## 👨‍💻 Autor

Proyecto desarrollado como trabajo práctico de Técnicas de Programación.

**Repositorio**: `Arnwaldsine/tp_tecnicas_programacion`

---

## 🔄 Flujo Completo del Sistema (Diagrama)

```
┌─────────────────────────────────────────────────────────┐
│                    MENÚ PRINCIPAL                       │
└─────────────────────────────────────────────────────────┘
              │
    ┌─────────┼─────────┬──────────────┬─────────┐
    │         │         │              │         │
    v         v         v              v         v
┌──────┐   ┌──────┐   ┌───────┐   ┌───────┐   ┌─────┐
│  1   │   │  2   │   │   3   │   │   4   │   │  5  │
│Buscar│   │Vender│   │Reponer│   │Ranking│   │Salir│
└──────┘   └──────┘   └───────┘   └───────┘   └─────┘
    │         │         │             │          │
    ├─Tipo    ├─Paginar ├─Paginar     └─Query    └─exit()
    ├─Marca   ├─Buscar  ├─Buscar        ORDER BY
    └─Modelo  ├─Vender  └─Reponer       ventas DESC
              │
              ├─Cantidad
              ├─Validar Stock
              ├─Tarjeta
              ├─Validar Formato
              ├─Confirmar
              └─UPDATE BD
```

---

## 📚 Recursos Adicionales

### Comandos Útiles

```bash
# Crear base de datos desde cero
python crear_base.py

# Ejecutar sistema
python gestion.py

# Acceder a BD manualmente (opcional)
sqlite3 inventario.db
sqlite> SELECT * FROM productos;
```

### Estructura de Imports

```python
# gestion.py
from queries import gestion_queries as q
from helpers import (
    clear_screen, conectar_db, mostrar_resultados,
    listar_tipos, listar_marcas, validar_tarjeta,
    seleccionar_producto_para_venta,
    seleccionar_producto_para_reponer
)

# helpers.py
from queries import gestion_queries as q

# crear_base.py
from queries import crear_base_queries as q
```

---

## 🎓 Conceptos Aplicados

- ✅ **Arquitectura Modular**: Separación de responsabilidades
- ✅ **Base de Datos Relacional**: Normalización, FK, JOINs
- ✅ **Paginación**: Manejo eficiente de grandes datasets
- ✅ **Validaciones**: Integridad de datos
- ✅ **UX/UI**: Interfaz intuitiva con colores y navegación
- ✅ **Manejo de Errores**: Try/except/finally, rollback
- ✅ **SQL Seguro**: Prepared statements (evita SQL injection)
- ✅ **Type Hints**: Mejor documentación y autocompletado
- ✅ **DRY Principle**: Reutilización de código (helpers)

---

¡El sistema está completamente documentado y listo para usar! 🚀