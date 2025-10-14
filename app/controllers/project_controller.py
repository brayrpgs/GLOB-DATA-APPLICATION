from datetime import date
from decimal import Decimal
from fastapi import HTTPException
from asyncpg import Pool
from app.repository.project_repository import ProjectRepository
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def post_project_controller(
    db_pool: Pool,
    name: Optional[str] = None,
    description: Optional[str] = None,
    user_project_id_fk: Optional[int] = None,
    date_init: Optional[date] = None,
    date_end: Optional[date] = None,
    status: Optional[int] = None,
    progress: Optional[Decimal] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = ProjectRepository(db_pool)
    try:
        return await repo.post_project(name, description, user_project_id_fk, date_init, date_end, status, progress)
    except Exception as e:
        logger.exception("Error en post_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


async def get_project_controller(db_pool: Pool, filters: dict, page: int, limit: int):
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    try:
        data = await ProjectRepository(db_pool).get_project(**filters, page=page, limit=limit)
        return {"data": data["data"], "page": page, "currentLimit": limit, "totalData": len(data["data"])}
    except Exception as e:
        logger.exception("Error en get_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def patch_project_controller(
    db_pool: Pool,
    project_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    user_project_id_fk: Optional[int] = None,
    date_init: Optional[date] = None,
    date_end: Optional[date] = None,
    status: Optional[int] = None,
    progress: Optional[Decimal] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = ProjectRepository(db_pool)
    try:
        return await repo.patch_project(project_id, name, description, user_project_id_fk, date_init, date_end, status, progress)
    except Exception as e:
        logger.exception("Error en patch_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def put_project_controller(
    db_pool: Pool,
    project_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    user_project_id_fk: Optional[int] = None,
    date_init: Optional[date] = None,
    date_end: Optional[date] = None,
    status: Optional[int] = None,
    progress: Optional[Decimal] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = ProjectRepository(db_pool)
    try:
        return await repo.put_project(project_id, name, description, user_project_id_fk, date_init, date_end, status, progress)
    except Exception as e:
        logger.exception("Error en put_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


async def delete_project_controller(db_pool: Pool, project_id: int):
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    try:
        return await ProjectRepository(db_pool).delete_project(project_id)
    except Exception as e:
        logger.exception("Error en delete_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
