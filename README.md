# 🔧 FerreApp - API de Gestión de Productos de Ferretería

## 📋 Descripción del Proyecto

**FerreApp** es una API REST desarrollada con **FastAPI** para resolver los problemas de gestión de inventario de la ferretería **Ferremax** de Don Carlos.

### Problemática

Don Carlos necesita un sistema moderno que le permita:

- **Registrar** nuevos productos en su inventario.
- **Consultar** el inventario en tiempo real.
- **Actualizar** precios y stock de productos existentes.
- **Eliminar** productos descontinuados.

### Solución

Una API REST que expone endpoints CRUD completos, con validación de datos mediante **Pydantic** y acceso a datos con **SQL nativo** (sin ORM), utilizando **SQLite** como base de datos.

---

## 🏗️ Estructura del Proyecto

```
ejercicio3_ferreapp_guiado/
├── app/
│   ├── __init__.py
│   ├── main.py            # Aplicación FastAPI con endpoints CRUD
│   └── database.py        # Acceso a datos con SQL nativo (sin ORM)
├── docs/
│   └── init_db.sql         # Script SQL de creación de tabla y datos iniciales
├── tests/
│   ├── __init__.py
│   ├── test_insertar.py    # Test de inserción de productos
│   ├── test_leer.py        # Test de lectura de productos
│   └── test_endpoints.py   # Test completo de la API (todos los endpoints)
├── requirements.txt        # Dependencias del proyecto
└── README.md               # Documentación del proyecto
```

---

## 🚀 Instalación y Ejecución

### 1. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la API

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: **http://127.0.0.1:8000**

### 4. Acceder a la documentación interactiva

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📡 Endpoints de la API

| Método   | Ruta                  | Descripción                     |
|----------|-----------------------|---------------------------------|
| `GET`    | `/`                   | Bienvenida a la API             |
| `GET`    | `/productos`          | Listar todos los productos      |
| `GET`    | `/productos/{id}`     | Obtener un producto por ID      |
| `POST`   | `/productos`          | Crear un nuevo producto         |
| `PUT`    | `/productos/{id}`     | Actualizar un producto existente|
| `DELETE` | `/productos/{id}`     | Eliminar un producto            |

### Ejemplo de cuerpo JSON (POST / PUT)

```json
{
    "nombre": "Martillo de Uña",
    "descripcion": "Martillo de acero forjado con mango ergonómico",
    "precio": 12500.00,
    "stock": 50,
    "categoria": "Herramientas Manuales",
    "sku": "HM-MART-001"
}
```

---

## 📐 Modelo de Datos (Validación Pydantic)

| Campo         | Tipo    | Validación                         |
|---------------|---------|------------------------------------|
| `id`          | int     | Autogenerado por la BD             |
| `nombre`      | str     | Obligatorio, 1-100 caracteres      |
| `descripcion` | str     | Obligatorio, 1-500 caracteres      |
| `precio`      | float   | Obligatorio, mayor a 0             |
| `stock`       | int     | Obligatorio, mayor o igual a 0     |
| `categoria`   | str     | Obligatorio, 1-100 caracteres      |
| `sku`         | str     | Obligatorio, único, 1-50 caracteres|

---

## 🧪 Ejecución de Tests

```bash
# Test de inserción
python tests/test_insertar.py

# Test de lectura
python tests/test_leer.py

# Test completo de endpoints
python tests/test_endpoints.py
```

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.12+**
- **FastAPI** — Framework web moderno y de alto rendimiento
- **Pydantic** — Validación de datos con modelos tipados
- **SQLite** — Base de datos embebida (sin necesidad de servidor externo)
- **Uvicorn** — Servidor ASGI para ejecutar la aplicación
- **SQL Nativo** — Consultas directas sin ORM

---

## 📄 Licencia

Proyecto educativo — Uso académico.
