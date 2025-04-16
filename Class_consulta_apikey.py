# api_key_manager.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import secrets
from typing import Optional, Dict, Any, List, Union


class ApiKeyManager:
    """
    Clase para gestionar operaciones de API keys en la base de datos MySQL.
    """

    def __init__(self, db_config: Dict[str, str]):
        """
        Inicializa el gestor con la configuración de la base de datos.

        Args:
            db_config: Diccionario con la configuración de conexión a MySQL
        """
        self.db_config = db_config

    def get_connection(self):
        """
        Establece una conexión a la base de datos MySQL.

        Returns:
            Conexión a la base de datos o None si hay error
        """
        try:
            conn = mysql.connector.connect(**self.db_config)
            return conn
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None

    def verify_api_key(self, key_value: str) -> Union[Dict[str, Any], None]:
        """
        Verifica si una API key es válida y no ha expirado.

        Args:
            key_value: El valor de la API key a verificar

        Returns:
            Diccionario con la información de la API key si es válida, None si no lo es
        """
        conn = self.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)

            query = """
            SELECT * FROM api_key 
            WHERE key_value = %s 
            AND is_active = 1 
            AND (expires_at IS NULL OR expires_at > NOW())
            """
            cursor.execute(query, (key_value,))
            result = cursor.fetchone()

            if result:
                # Actualizar el último uso de la API key
                update_query = """
                UPDATE api_key SET last_used_at = NOW() 
                WHERE key_value = %s
                """
                cursor.execute(update_query, (key_value,))
                conn.commit()

            return result

        except Error as e:
            print(f"Error en la consulta: {e}")
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def create_api_key(self, user_id: int, key_name: str,
                       expires_at: Optional[datetime] = None,
                       is_admin: bool = False) -> Optional[str]:
        """
        Crea una nueva API key para un usuario.

        Args:
            user_id: ID del usuario asociado a la API key
            key_name: Nombre descriptivo de la API key
            expires_at: Fecha de expiración (opcional)
            is_admin: Si la clave tiene permisos de administrador

        Returns:
            El valor de la nueva API key o None si hay error
        """
        conn = self.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()

            # Generar una nueva API key
            new_api_key = secrets.token_urlsafe(32)

            query = """
            INSERT INTO api_key 
            (user_id, key_name, key_value, created_at, expires_at, is_active, is_admin) 
            VALUES (%s, %s, %s, NOW(), %s, 1, %s)
            """

            cursor.execute(query, (user_id, key_name, new_api_key, expires_at, is_admin))
            conn.commit()

            return new_api_key

        except Error as e:
            print(f"Error al crear API key: {e}")
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def revoke_api_key(self, key_value: str) -> bool:
        """
        Revoca una API key marcándola como inactiva.

        Args:
            key_value: El valor de la API key a revocar

        Returns:
            True si se revocó correctamente, False en caso contrario
        """
        conn = self.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()

            query = """
            UPDATE api_key SET is_active = 0, revoked_at = NOW()
            WHERE key_value = %s
            """

            cursor.execute(query, (key_value,))
            conn.commit()

            return cursor.rowcount > 0

        except Error as e:
            print(f"Error al revocar API key: {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def get_user_api_keys(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Obtiene todas las API keys activas de un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            Lista de diccionarios con la información de cada API key
        """
        conn = self.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)

            query = """
            SELECT id, key_name, created_at, last_used_at, expires_at, is_admin 
            FROM api_key 
            WHERE user_id = %s AND is_active = 1
            ORDER BY created_at DESC
            """

            cursor.execute(query, (user_id,))
            return cursor.fetchall()

        except Error as e:
            print(f"Error al obtener API keys: {e}")
            return []
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()