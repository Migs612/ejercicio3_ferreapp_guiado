-- ============================================
-- FerreApp - Ferremax
-- Script de Inicialización de Base de Datos
-- ============================================

-- Crear la tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    precio REAL NOT NULL CHECK(precio >= 0),
    stock INTEGER NOT NULL CHECK(stock >= 0),
    categoria TEXT NOT NULL,
    sku TEXT NOT NULL UNIQUE
);

-- Datos de ejemplo para pruebas iniciales
INSERT INTO productos (nombre, descripcion, precio, stock, categoria, sku)
VALUES
    ('Martillo de Uña', 'Martillo de acero forjado con mango ergonómico', 12500.00, 50, 'Herramientas Manuales', 'HM-MART-001'),
    ('Destornillador Phillips', 'Destornillador Phillips #2, mango antideslizante', 5500.00, 120, 'Herramientas Manuales', 'HM-DEST-002'),
    ('Taladro Inalámbrico 20V', 'Taladro percutor inalámbrico con batería de litio', 89990.00, 15, 'Herramientas Eléctricas', 'HE-TALD-001'),
    ('Cemento Portland 25kg', 'Saco de cemento portland gris de 25 kilogramos', 8500.00, 200, 'Materiales de Construcción', 'MC-CEME-001'),
    ('Pintura Látex Blanca 4L', 'Pintura látex interior/exterior color blanco', 18900.00, 80, 'Pinturas', 'PI-LATE-001'),
    ('Cinta Métrica 5m', 'Cinta métrica profesional de 5 metros con freno', 4200.00, 95, 'Herramientas de Medición', 'HME-CINT-001'),
    ('Llave Ajustable 10"', 'Llave ajustable cromada de 10 pulgadas', 9800.00, 40, 'Herramientas Manuales', 'HM-LLAV-003'),
    ('Sierra Circular 7 1/4"', 'Sierra circular eléctrica de 1800W', 75000.00, 10, 'Herramientas Eléctricas', 'HE-SIER-002');
