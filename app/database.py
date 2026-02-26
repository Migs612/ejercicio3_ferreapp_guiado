"""
FerreApp - Módulo de Acceso a Datos
====================================
Gestión de la base de datos SQLite usando SQL nativo.
No se utiliza ORM: todas las operaciones se realizan con consultas SQL directas.
"""

import sqlite3
import os

# Ruta de la base de datos SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "ferremax.db")
SQL_INIT_PATH = os.path.join(BASE_DIR, "docs", "init_db.sql")


def get_connection() -> sqlite3.Connection:
    """
    Crea y retorna una conexión a la base de datos SQLite.
    Configura row_factory para obtener resultados como diccionarios.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Inicializa la base de datos ejecutando el script SQL de creación.
    Solo crea la tabla si no existe previamente.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si la tabla ya tiene datos
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='productos'"
    )
    table_exists = cursor.fetchone()

    if not table_exists:
        # Leer y ejecutar el script SQL de inicialización
        with open(SQL_INIT_PATH, "r", encoding="utf-8") as f:
            sql_script = f.read()
        cursor.executescript(sql_script)
        conn.commit()
        print("✔ Base de datos inicializada con datos de ejemplo.")
    else:
        print("ℹ La tabla 'productos' ya existe. No se reinicializa.")

    conn.close()


# ============================================
# FUNCIONES CRUD - SQL NATIVO
# ============================================


def obtener_todos_los_productos() -> list[dict]:
    """Obtiene todos los productos de la base de datos."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return productos


def obtener_producto_por_id(producto_id: int) -> dict | None:
    """Obtiene un producto por su ID. Retorna None si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def crear_producto(nombre: str, descripcion: str, precio: float,
                   stock: int, categoria: str, sku: str) -> dict:
    """
    Inserta un nuevo producto en la base de datos.
    Retorna el producto creado con su ID asignado.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO productos (nombre, descripcion, precio, stock, categoria, sku)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (nombre, descripcion, precio, stock, categoria, sku)
    )
    conn.commit()
    producto_id = cursor.lastrowid
    conn.close()
    return obtener_producto_por_id(producto_id)


def actualizar_producto(producto_id: int, nombre: str, descripcion: str,
                        precio: float, stock: int, categoria: str,
                        sku: str) -> dict | None:
    """
    Actualiza un producto existente por su ID.
    Retorna el producto actualizado o None si no existe.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE productos
        SET nombre = ?, descripcion = ?, precio = ?, stock = ?, categoria = ?, sku = ?
        WHERE id = ?
        """,
        (nombre, descripcion, precio, stock, categoria, sku, producto_id)
    )
    conn.commit()
    filas_afectadas = cursor.rowcount
    conn.close()

    if filas_afectadas == 0:
        return None
    return obtener_producto_por_id(producto_id)


def eliminar_producto(producto_id: int) -> bool:
    """
    Elimina un producto por su ID.
    Retorna True si se eliminó, False si no existía.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conn.commit()
    filas_afectadas = cursor.rowcount
    conn.close()
    return filas_afectadas > 0
