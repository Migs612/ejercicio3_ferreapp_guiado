"""
Test de Inserción de Productos
===============================
Verifica que se puedan insertar productos correctamente
en la base de datos usando SQL nativo.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db, crear_producto, obtener_todos_los_productos, eliminar_producto


def test_insertar_producto():
    """Prueba la inserción de un producto nuevo."""
    print("=" * 50)
    print("TEST: Inserción de Producto")
    print("=" * 50)

    # Inicializar la base de datos
    init_db()

    # Datos del producto de prueba
    producto_test = {
        "nombre": "Producto de Prueba",
        "descripcion": "Este es un producto insertado desde el test",
        "precio": 9999.99,
        "stock": 25,
        "categoria": "Test",
        "sku": "TEST-INS-001",
    }

    # Insertar el producto
    print(f"\n📦 Insertando producto: {producto_test['nombre']}")
    nuevo = crear_producto(**producto_test)

    if nuevo:
        print(f"✅ Producto creado exitosamente:")
        print(f"   ID: {nuevo['id']}")
        print(f"   Nombre: {nuevo['nombre']}")
        print(f"   Precio: ${nuevo['precio']:,.2f}")
        print(f"   Stock: {nuevo['stock']} unidades")
        print(f"   SKU: {nuevo['sku']}")
    else:
        print("❌ Error: No se pudo crear el producto")
        return False

    # Verificar que se insertó consultando todos los productos
    todos = obtener_todos_los_productos()
    encontrado = any(p["sku"] == "TEST-INS-001" for p in todos)

    if encontrado:
        print(f"\n✅ Verificación: Producto encontrado en la base de datos")
    else:
        print(f"\n❌ Verificación fallida: Producto no encontrado")
        return False

    # Limpiar: eliminar el producto de prueba
    eliminado = eliminar_producto(nuevo["id"])
    if eliminado:
        print(f"🧹 Limpieza: Producto de prueba eliminado (ID: {nuevo['id']})")

    print("\n✅ TEST DE INSERCIÓN COMPLETADO EXITOSAMENTE")
    return True


if __name__ == "__main__":
    exito = test_insertar_producto()
    sys.exit(0 if exito else 1)
