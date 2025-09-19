from os import getenv
import asyncpg

_pool: asyncpg.Pool | None = None

def get_db_config() -> dict:
    """Returns the DB connection configuration from environment variables."""
    return {
        "host": getenv("POSTGRES_HOST"),
        "port": 5432,
        "database": getenv("POSTGRES_DB"),
        "user": getenv("POSTGRES_USER"),
        "password": getenv("POSTGRES_PASSWORD")
    }

async def init_pool() -> asyncpg.Pool:
    """Initializes the connection pool if it does not already exist."""
    global _pool
    if _pool is None:
        config = get_db_config()
        _pool = await asyncpg.create_pool(**config)
    return _pool

def get_pool() -> asyncpg.Pool:
    """Returns the connection pool. Throws an error if it has not been initialized."""
    if _pool is None:
        raise RuntimeError("Connection pool is not initialized. Call init_pool() first.")
    return _pool

async def close_pool():
    """Closes the connection pool if it exists."""
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
