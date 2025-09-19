from datetime import date
from typing import Optional
from asyncpg import Pool
from fastapi import HTTPException
from app.repository.sprint_repository import SprintRepository
import logging

logger = logging.getLogger(__name__)

async def get_sprint_controller(
    db_pool: Pool,
    sprint_id: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    date_init_start: Optional[str] = None,
    date_init_end: Optional[str] = None,
    date_end_start: Optional[str] = None,
    date_end_end: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
):
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = SprintRepository(db_pool)
    return await repo.get_sprint(
        sprint_id,
        name,
        description,
        date_init_start,
        date_init_end,
        date_end_start,
        date_end_end,
        page,
        limit,
    )

async def post_sprint_controller(db_pool: Pool, sprint_data: dict):
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = SprintRepository(db_pool)
    params = (
        sprint_data.get("name"),
        sprint_data.get("description"),
        sprint_data.get("date_init"),
        sprint_data.get("date_end"),
    )
    return await repo.post_sprint(params)

async def patch_sprint_controller(
    db_pool: Pool,
    sprint_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    date_init: Optional[date] = None,
    date_end: Optional[date] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = SprintRepository(db_pool)
    try:
        return await repo.patch_sprint(sprint_id, name, description, date_init, date_end)
    except Exception as e:
        logger.exception("Error en patch_sprint_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def put_sprint_controller(
    db_pool: Pool,
    sprint_id: int,
    name: str,
    description: str,
    date_init: date,
    date_end: date
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = SprintRepository(db_pool)
    try:
        return await repo.put_sprint(sprint_id, name, description, date_init, date_end)
    except Exception as e:
        logger.exception("Error en put_sprint_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def delete_sprint_controller(db_pool: Pool, sprint_id: int) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = SprintRepository(db_pool)
    try:
        return await repo.delete_sprint(sprint_id)
    except Exception as e:
        logger.exception("Error en delete_sprint_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))