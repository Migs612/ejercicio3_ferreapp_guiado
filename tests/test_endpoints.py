"""
Test de Endpoints de la API
=============================
Verifica que los endpoints de la API respondan correctamente
usando el TestClient de FastAPI.
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_endpoint_inicio():
    """Verifica el endpoint de bienvenida."""
    print("=" * 50)
    print("TEST: Endpoint GET /")
    print("=" * 50)

    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "mensaje" in data
    print(f"✅ GET / → {response.status_code}: {data['mensaje']}")
    return True


def test_endpoint_listar_productos():
    """Verifica el endpoint de listado de productos."""
    print("\n" + "=" * 50)
    print("TEST: Endpoint GET /productos")
    print("=" * 50)

    response = client.get("/productos")
    assert response.status_code == 200
    productos = response.json()
    assert isinstance(productos, list)
    print(f"✅ GET /productos → {response.status_code}: {len(productos)} productos")
    return True


def test_endpoint_crear_producto():
    """Verifica el endpoint de creación de producto."""
    print("\n" + "=" * 50)
    print("TEST: Endpoint POST /productos")
    print("=" * 50)

    nuevo_producto = {
        "nombre": "Producto API Test",
        "descripcion": "Producto creado desde test de endpoint",
        "precio": 15000.0,
        "stock": 30,
        "categoria": "Test API",
        "sku": "TEST-API-001",
    }

    response = client.post("/productos", json=nuevo_producto)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == nuevo_producto["nombre"]
    assert "id" in data
    print(f"✅ POST /productos → {response.status_code}: Creado ID {data['id']}")

    # Guardar ID para limpieza
    return data["id"]


def test_endpoint_obtener_producto(producto_id: int):
    """Verifica el endpoint de obtención de producto por ID."""
    print("\n" + "=" * 50)
    print(f"TEST: Endpoint GET /productos/{producto_id}")
    print("=" * 50)

    response = client.get(f"/productos/{producto_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == producto_id
    print(f"✅ GET /productos/{producto_id} → {response.status_code}: {data['nombre']}")
    return True


def test_endpoint_actualizar_producto(producto_id: int):
    """Verifica el endpoint de actualización de producto."""
    print("\n" + "=" * 50)
    print(f"TEST: Endpoint PUT /productos/{producto_id}")
    print("=" * 50)

    producto_actualizado = {
        "nombre": "Producto API Test Actualizado",
        "descripcion": "Producto actualizado desde test de endpoint",
        "precio": 18500.0,
        "stock": 45,
        "categoria": "Test API",
        "sku": "TEST-API-001",
    }

    response = client.put(f"/productos/{producto_id}", json=producto_actualizado)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == producto_actualizado["nombre"]
    assert data["precio"] == producto_actualizado["precio"]
    print(f"✅ PUT /productos/{producto_id} → {response.status_code}: Actualizado")
    return True


def test_endpoint_eliminar_producto(producto_id: int):
    """Verifica el endpoint de eliminación de producto."""
    print("\n" + "=" * 50)
    print(f"TEST: Endpoint DELETE /productos/{producto_id}")
    print("=" * 50)

    response = client.delete(f"/productos/{producto_id}")
    assert response.status_code == 200
    data = response.json()
    assert "mensaje" in data
    print(f"✅ DELETE /productos/{producto_id} → {response.status_code}: {data['mensaje']}")
    return True


def test_endpoint_producto_no_existe():
    """Verifica que la API retorne 404 para un producto inexistente."""
    print("\n" + "=" * 50)
    print("TEST: Endpoint GET /productos/99999 (No existe)")
    print("=" * 50)

    response = client.get("/productos/99999")
    assert response.status_code == 404
    print(f"✅ GET /productos/99999 → {response.status_code}: Producto no encontrado (esperado)")
    return True


def test_endpoint_validacion():
    """Verifica que Pydantic valide los datos correctamente."""
    print("\n" + "=" * 50)
    print("TEST: Validación Pydantic (precio negativo)")
    print("=" * 50)

    producto_invalido = {
        "nombre": "Producto Inválido",
        "descripcion": "Test de validación",
        "precio": -100.0,  # Precio negativo: debe fallar
        "stock": 10,
        "categoria": "Test",
        "sku": "TEST-VAL-001",
    }

    response = client.post("/productos", json=producto_invalido)
    assert response.status_code == 422  # Unprocessable Entity
    print(f"✅ POST /productos (inválido) → {response.status_code}: Validación rechazó precio negativo")
    return True


if __name__ == "__main__":
    print("🔧 FERREAPP - Suite de Tests de Endpoints\n")

    test_endpoint_inicio()
    test_endpoint_listar_productos()

    # CRUD completo
    producto_id = test_endpoint_crear_producto()
    test_endpoint_obtener_producto(producto_id)
    test_endpoint_actualizar_producto(producto_id)
    test_endpoint_eliminar_producto(producto_id)

    # Casos de error
    test_endpoint_producto_no_existe()
    test_endpoint_validacion()

    print("\n" + "=" * 50)
    print("🎉 TODOS LOS TESTS PASARON EXITOSAMENTE")
    print("=" * 50)
