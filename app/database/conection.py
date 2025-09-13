from os import getenv
import asyncpg

_pool: asyncpg.Pool | None = None

def get_db_config() -> dict:
    """Devuelve la configuración de la conexión a la DB desde variables de entorno."""
    return {
        "host": getenv("POSTGRES_HOST"),
        "port": 5432,
        "database": getenv("POSTGRES_DB"),
        "user": getenv("POSTGRES_USER"),
        "password": getenv("POSTGRES_PASSWORD")
    }

async def init_pool() -> asyncpg.Pool:
    """Inicializa el pool de conexiones si aún no existe."""
    global _pool
    if _pool is None:
        config = get_db_config()
        _pool = await asyncpg.create_pool(**config)
    return _pool

def get_pool() -> asyncpg.Pool:
    """Devuelve el pool de conexiones. Lanza error si no se inicializó."""
    if _pool is None:
        raise RuntimeError("Connection pool is not initialized. Call init_pool() first.")
    return _pool

async def close_pool():
    """Cierra el pool de conexiones si existe."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
