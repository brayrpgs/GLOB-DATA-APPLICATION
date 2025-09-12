import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from os import getenv

# Función pura que devuelve la configuración de la conexión
def get_db_config() -> dict:
    return {
        "host": getenv("POSTGRES_HOST"),
        "port": 5432,
        "database": getenv("POSTGRES_DB"),
        "user": getenv("POSTGRES_USER"),
        "password": getenv("POSTGRES_PASSWORD")
    }

# Context manager para obtener la conexión (manejo funcional)
@contextmanager
def get_connection():
    config = get_db_config()
    print("Database connection config:", config)  # Temporary print for debugging
    conn = psycopg2.connect(**config, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()