from typing import Optional
from fastapi import HTTPException
from asyncpg import Pool
from app.repository.issue_type import IssueTypeRepository
import logging

logger = logging.getLogger(__name__)

async def post_issue_type_controller(db_pool: Pool, status: int, priority: int) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = IssueTypeRepository(db_pool)
    try:
        return await repo.post_issue_type(status, priority)
    except Exception as e:
        logger.exception("Error en post_issue_type_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def get_issue_type_controller(
    db_pool: Pool,
    issue_type_id: Optional[int] = None,
    status: Optional[int] = None,
    priority: Optional[int] = None,
    page: int = 1,
    limit: int = 10
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = IssueTypeRepository(db_pool)
    try:
        data = await repo.get_issue_type(issue_type_id, status, priority, page, limit)
        return {"data": data, "page": page, "currentLimit": limit, "totalData": len(data)}
    except Exception as e:
        logger.exception("Error en get_issue_type_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def patch_issue_type_controller(
    db_pool: Pool,
    issue_type_id: int,
    status: Optional[int] = None,
    priority: Optional[int] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = IssueTypeRepository(db_pool)
    try:
        return await repo.patch_issue_type(issue_type_id, status, priority)
    except Exception as e:
        logger.exception("Error en patch_issue_type_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def put_issue_type_controller(db_pool: Pool, issue_type_id: int, status: int, priority: int) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = IssueTypeRepository(db_pool)
    try:
        return await repo.put_issue_type(issue_type_id, status, priority)
    except Exception as e:
        logger.exception("Error en put_issue_type_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def delete_issue_type_controller(db_pool: Pool, issue_type_id: int) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = IssueTypeRepository(db_pool)
    try:
        return await repo.delete_issue_type(issue_type_id)
    except Exception as e:
        logger.exception("Error en delete_issue_type_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
