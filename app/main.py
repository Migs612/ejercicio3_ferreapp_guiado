"""
FerreApp - API REST de Gestión de Productos
=============================================
API para la ferretería Ferremax de Don Carlos.
Permite el registro, consulta de inventario en tiempo real
y actualización de precios mediante endpoints REST.

Autor: Manuel Ignacio
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.database import (
    init_db,
    obtener_todos_los_productos,
    obtener_producto_por_id,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
)

# ============================================
# Inicialización de la aplicación FastAPI
# ============================================

app = FastAPI(
    title="FerreApp - Ferremax API",
    description=(
        "API REST para la gestión de productos de la ferretería Ferremax. "
        "Permite realizar operaciones CRUD completas sobre el inventario de productos."
    ),
    version="1.0.0",
)

# Inicializar la base de datos al arrancar la aplicación
init_db()


# ============================================
# Modelos Pydantic para validación de datos
# ============================================


class ProductoBase(BaseModel):
    """Esquema base para validación de datos de producto."""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    descripcion: str = Field(..., min_length=1, max_length=500, description="Descripción del producto")
    precio: float = Field(..., gt=0, description="Precio del producto (debe ser mayor a 0)")
    stock: int = Field(..., ge=0, description="Cantidad en stock (debe ser >= 0)")
    categoria: str = Field(..., min_length=1, max_length=100, description="Categoría del producto")
    sku: str = Field(..., min_length=1, max_length=50, description="Código SKU único del producto")


class ProductoResponse(ProductoBase):
    """Esquema de respuesta que incluye el ID del producto."""
    id: int = Field(..., description="Identificador único del producto")

    class Config:
        from_attributes = True


# ============================================
# Endpoints de la API
# ============================================


@app.get("/", tags=["Inicio"])
def inicio():
    """Endpoint de bienvenida a la API de Ferremax."""
    return {
        "mensaje": "Bienvenido a la API de Ferremax 🔧",
        "descripcion": "Sistema de gestión de productos de ferretería",
        "documentacion": "/docs",
    }


@app.get("/productos", response_model=list[ProductoResponse], tags=["Productos"])
def listar_productos():
    """
    Obtener todos los productos.

    Retorna la lista completa de productos disponibles en el inventario.
    """
    productos = obtener_todos_los_productos()
    return productos


@app.get("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
def obtener_producto(producto_id: int):
    """
    Obtener un producto por su ID.

    - **producto_id**: ID del producto a consultar.
    """
    producto = obtener_producto_por_id(producto_id)
    if producto is None:
        raise HTTPException(
            status_code=404,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return producto


@app.post("/productos", response_model=ProductoResponse, status_code=201, tags=["Productos"])
def crear_nuevo_producto(producto: ProductoBase):
    """
    Crear un nuevo producto.

    Registra un nuevo producto en el inventario de Ferremax.
    Todos los campos son obligatorios y se validan automáticamente.
    """
    try:
        nuevo_producto = crear_producto(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            stock=producto.stock,
            categoria=producto.categoria,
            sku=producto.sku,
        )
        return nuevo_producto
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(
                status_code=400,
                detail=f"El SKU '{producto.sku}' ya existe en la base de datos"
            )
        raise HTTPException(status_code=500, detail=f"Error al crear el producto: {str(e)}")


@app.put("/productos/{producto_id}", response_model=ProductoResponse, tags=["Productos"])
def actualizar_producto_existente(producto_id: int, producto: ProductoBase):
    """
    Actualizar un producto existente.

    - **producto_id**: ID del producto a actualizar.
    - Requiere enviar todos los campos del producto.
    """
    try:
        producto_actualizado = actualizar_producto(
            producto_id=producto_id,
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            stock=producto.stock,
            categoria=producto.categoria,
            sku=producto.sku,
        )
        if producto_actualizado is None:
            raise HTTPException(
                status_code=404,
                detail=f"Producto con ID {producto_id} no encontrado"
            )
        return producto_actualizado
    except HTTPException:
        raise
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(
                status_code=400,
                detail=f"El SKU '{producto.sku}' ya está asignado a otro producto"
            )
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {str(e)}")


@app.delete("/productos/{producto_id}", tags=["Productos"])
def eliminar_producto_existente(producto_id: int):
    """
    Eliminar un producto.

    - **producto_id**: ID del producto a eliminar.
    """
    eliminado = eliminar_producto(producto_id)
    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return {"mensaje": f"Producto con ID {producto_id} eliminado exitosamente"}
