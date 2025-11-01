# Queries reutilizables para la lógica de gestión

# Listados
SELECT_TODAS_MARCAS = "SELECT id, nombre FROM marcas ORDER BY id"
SELECT_TODOS_TIPOS = "SELECT id, nombre FROM tipos_producto ORDER BY id"

# Búsquedas (con JOIN para obtener marca/tipo)
SELECT_POR_TIPO = """
SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
FROM productos p
LEFT JOIN marcas m ON p.marca_id = m.id
LEFT JOIN tipos_producto t ON p.tipo_id = t.id
WHERE p.tipo_id = ?
ORDER BY p.id
"""

SELECT_POR_MARCA = """
SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
FROM productos p
LEFT JOIN marcas m ON p.marca_id = m.id
LEFT JOIN tipos_producto t ON p.tipo_id = t.id
WHERE p.marca_id = ?
ORDER BY p.id
"""

SELECT_POR_MODELO_LIKE = """
SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
FROM productos p
LEFT JOIN marcas m ON p.marca_id = m.id
LEFT JOIN tipos_producto t ON p.tipo_id = t.id
WHERE LOWER(p.modelo) LIKE ?
ORDER BY p.id
"""

SELECT_MODELO_EXACTO = """
SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
FROM productos p
LEFT JOIN marcas m ON p.marca_id = m.id
LEFT JOIN tipos_producto t ON p.tipo_id = t.id
WHERE LOWER(p.modelo) = ?
"""

SELECT_MAS_VENDIDOS = """
SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
FROM productos p
LEFT JOIN marcas m ON p.marca_id = m.id
LEFT JOIN tipos_producto t ON p.tipo_id = t.id
WHERE p.ventas > 0
ORDER BY p.ventas DESC, p.id
"""

# Actualizaciones
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

# Nuevas queries para la sección de ventas (paginación y búsqueda con stock disponible)
SELECT_PRODUCTOS_DISPONIBLES_PAGINATED = """
SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
FROM productos p
LEFT JOIN marcas m ON p.marca_id = m.id
LEFT JOIN tipos_producto t ON p.tipo_id = t.id
WHERE p.stock > 0
ORDER BY LOWER(p.modelo)
LIMIT ? OFFSET ?
"""

# Búsqueda entre productos con stock > 0 (no paginada en SQL; límite aplicado en la UI si hace falta)
SELECT_PRODUCTOS_DISPONIBLES_BUSCAR = """
SELECT p.id, p.modelo, p.precio, p.stock, p.ventas, m.nombre, t.nombre
FROM productos p
LEFT JOIN marcas m ON p.marca_id = m.id
LEFT JOIN tipos_producto t ON p.tipo_id = t.id
WHERE p.stock > 0 AND LOWER(p.modelo) LIKE ?
ORDER BY LOWER(p.modelo)
LIMIT ?
"""