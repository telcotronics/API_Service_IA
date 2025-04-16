Script SQL para crear la tabla api_key
Código
Esta implementación te proporciona:

Una clase ApiKeyManager separada que maneja todas las operaciones de API keys con la base de datos
Una aplicación FastAPI que utiliza esta clase para la autenticación
Endpoints para crear, listar y revocar API keys (solo para administradores)
Un script SQL para crear la tabla necesaria en MySQL
Para usar este sistema:

Instala las dependencias: pip install fastapi uvicorn mysql-connector-python
Crea la tabla en tu base de datos MySQL usando el script proporcionado
Ajusta los parámetros de conexión a la base de datos en DB_CONFIG
Ejecuta la aplicación: uvicorn main:app --reload
¿Hay alguna característica adicional que quieras implementar o algo que te gustaría modificar en este diseño?

-- Script para crear la tabla api_key en MySQL

CREATE TABLE api_key (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    key_name VARCHAR(100) NOT NULL,
    key_value VARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL,
    last_used_at DATETIME NULL,
    expires_at DATETIME NULL,
    revoked_at DATETIME NULL,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    INDEX idx_user_id (user_id),
    INDEX idx_key_value (key_value)
);

-- Comentarios sobre los campos:
-- user_id: ID del usuario asociado a la API key
-- key_name: Nombre descriptivo de la API key (ej. "", "Producción")
-- key_value: El valor real de la API key que se usará en las solicitudes
-- created_at: Fecha y hora de creación de la API key
-- last_used_at: Fecha y hora del último uso
-- expires_at: Fecha y hora de expiración (NULL si no expira)
-- revoked_at: Fecha y hora en que fue revocada
-- is_active: Indica si la API key está activa (1) o revocada (0)
-- is_admin: Indica si la API key tiene privilegios de administrador

INSERT INTO api_key (
    id,
    user_id,
    key_name,
    key_value,
    created_at,
    last_used_at,
    expires_at,
    revoked_at,
    is_active,
    is_admin
) VALUES (
    1,                                              -- id (autoincremental)
    101,                                            -- user_id
    "API Desarrollo",                               -- key_name
    "ak_VVeNzGxK2mCq8s7YpFtHjL3b9dR4TuZ6",         -- key_value
    '2025-04-16 10:30:45',                          -- created_at
    '2025-04-16 14:22:18',                          -- last_used_at
    '2026-04-16 10:30:45',                          -- expires_at (expira en un año)
    NULL,                                           -- revoked_at (no revocada)
    1,                                              -- is_active (activa)
    0                                               -- is_admin (no es admin)
);