"""
Test de Lectura de Productos
==============================
Verifica que se puedan consultar productos correctamente
desde la base de datos usando SQL nativo.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db, obtener_todos_los_productos, obtener_producto_por_id


def test_leer_todos_los_productos():
    """Prueba la lectura de todos los productos."""
    print("=" * 50)
    print("TEST: Lectura de Todos los Productos")
    print("=" * 50)

    # Inicializar la base de datos
    init_db()

    # Obtener todos los productos
    productos = obtener_todos_los_productos()

    print(f"\n📋 Se encontraron {len(productos)} productos en la base de datos:\n")

    for p in productos:
        print(f"  [{p['id']}] {p['nombre']}")
        print(f"      Precio: ${p['precio']:,.2f} | Stock: {p['stock']} | SKU: {p['sku']}")
        print(f"      Categoría: {p['categoria']}")
        print()

    if len(productos) > 0:
        print(f"✅ Lectura masiva exitosa: {len(productos)} productos obtenidos")
    else:
        print("⚠️  No se encontraron productos (la base de datos puede estar vacía)")

    return True


def test_leer_producto_por_id():
    """Prueba la lectura de un producto específico por ID."""
    print("\n" + "=" * 50)
    print("TEST: Lectura de Producto por ID")
    print("=" * 50)

    # Buscar el producto con ID 1
    producto = obtener_producto_por_id(1)

    if producto:
        print(f"\n✅ Producto encontrado (ID: 1):")
        print(f"   Nombre: {producto['nombre']}")
        print(f"   Descripción: {producto['descripcion']}")
        print(f"   Precio: ${producto['precio']:,.2f}")
        print(f"   Stock: {producto['stock']} unidades")
        print(f"   Categoría: {producto['categoria']}")
        print(f"   SKU: {producto['sku']}")
    else:
        print("\n⚠️  Producto con ID 1 no encontrado")

    # Buscar un producto que no existe
    producto_inexistente = obtener_producto_por_id(99999)
    if producto_inexistente is None:
        print(f"\n✅ Verificación correcta: Producto con ID 99999 no existe (retorna None)")
    else:
        print(f"\n❌ Error: Se encontró un producto que no debería existir")
        return False

    print("\n✅ TEST DE LECTURA COMPLETADO EXITOSAMENTE")
    return True


if __name__ == "__main__":
    exito1 = test_leer_todos_los_productos()
    exito2 = test_leer_producto_por_id()
    sys.exit(0 if (exito1 and exito2) else 1)
