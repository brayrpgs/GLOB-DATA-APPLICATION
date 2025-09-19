from typing import Optional
from fastapi import HTTPException
from asyncpg import Pool
from app.repository.user_project import UserProjectRepository
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

async def post_user_project_controller(
    db_pool: Pool,
    user_id_fk: int,
    rol_proyect: int,
    productivity: Decimal
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = UserProjectRepository(db_pool)
    try:
        return await repo.post_user_project(user_id_fk, rol_proyect, productivity)
    except Exception as e:
        logger.exception("Error en post_user_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def get_user_project_controller(
    db_pool: Pool,
    user_project_id: Optional[int] = None,
    user_id_fk: Optional[int] = None,
    rol_proyect: Optional[int] = None,
    productivity: Optional[Decimal] = None,
    page: int = 1,
    limit: int = 10
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = UserProjectRepository(db_pool)
    try:
        data = await repo.get_user_project(user_project_id, user_id_fk, rol_proyect, productivity, page, limit)
        return {"data": data, "page": page, "currentLimit": limit, "totalData": len(data) if data else 0}
    except Exception as e:
        logger.exception("Error en get_user_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def patch_user_project_controller(
    db_pool: Pool,
    user_project_id: int,
    user_id_fk: Optional[int] = None,
    rol_proyect: Optional[int] = None,
    productivity: Optional[Decimal] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = UserProjectRepository(db_pool)
    try:
        return await repo.patch_user_project(user_project_id, user_id_fk, rol_proyect, productivity)
    except Exception as e:
        logger.exception("Error en patch_user_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def put_user_project_controller(
    db_pool: Pool,
    user_project_id: int,
    user_id_fk: int,
    rol_proyect: int,
    productivity: Decimal
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = UserProjectRepository(db_pool)
    try:
        return await repo.put_user_project(user_project_id, user_id_fk, rol_proyect, productivity)
    except Exception as e:
        logger.exception("Error en put_user_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def delete_user_project_controller(db_pool: Pool, user_project_id: int) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = UserProjectRepository(db_pool)
    try:
        return await repo.delete_user_project(user_project_id)
    except Exception as e:
        logger.exception("Error en delete_user_project_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))