# main.py

from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader, APIKey
from typing import Optional
from datetime import datetime

# Importamos nuestra clase ApiKeyManager
from Class_consulta_apikey import ApiKeyManager

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "user": "tu_usuario",
    "password": "tu_contraseña",
    "database": "tu_base_de_datos"
}

# Creamos una instancia del gestor de API keys
api_key_manager = ApiKeyManager(DB_CONFIG)

# Definimos nuestra aplicación FastAPI
app = FastAPI(title="API con sistema de API Keys usando MySQL")

# Definimos el esquema de seguridad para las API keys
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# Función para verificar la API key
async def get_api_key(api_key_header: str = Security(api_key_header)):
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key no proporcionada"
        )

    # Verificamos la API key usando nuestro gestor
    api_key_info = api_key_manager.verify_api_key(api_key_header)

    if not api_key_info:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key inválida o expirada"
        )

    return api_key_info


# Verificación adicional para endpoints de administración
async def get_admin_api_key(api_key_info: dict = Depends(get_api_key)):
    if not api_key_info.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de administrador"
        )
    return api_key_info


# Ruta protegida que requiere autenticación con API key
@app.get("/items/", tags=["Items"])
async def read_items(api_key_info: dict = Depends(get_api_key)):
    return {
        "message": "Has accedido correctamente a un endpoint protegido",
        "user_id": api_key_info.get("user_id"),
        "key_name": api_key_info.get("key_name")
    }


# Ruta pública sin protección
@app.get("/", tags=["Público"])
async def root():
    return {"message": "Bienvenido a la API. Para acceder a los endpoints protegidos necesitas una API key"}


# Endpoint para crear nuevas API keys (solo para administradores)
@app.post("/api-keys/", tags=["Admin"])
async def create_api_key(user_id: int, key_name: str,
                         expires_at: Optional[datetime] = None,
                         admin_info: dict = Depends(get_admin_api_key)):
    new_key = api_key_manager.create_api_key(
        user_id=user_id,
        key_name=key_name,
        expires_at=expires_at
    )

    if not new_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear la API key"
        )

    return {"key": new_key, "message": "API key creada correctamente"}


# Endpoint para listar las API keys de un usuario (solo para administradores)
@app.get("/users/{user_id}/api-keys/", tags=["Admin"])
async def list_user_api_keys(user_id: int, admin_info: dict = Depends(get_admin_api_key)):
    keys = api_key_manager.get_user_api_keys(user_id)
    return {"keys": keys}


# Endpoint para revocar una API key (solo para administradores)
@app.delete("/api-keys/{key_value}", tags=["Admin"])
async def revoke_api_key(key_value: str, admin_info: dict = Depends(get_admin_api_key)):
    success = api_key_manager.revoke_api_key(key_value)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key no encontrada o ya revocada"
        )

    return {"message": "API key revocada correctamente"}

# Para ejecutar: uvicorn main:app --reload