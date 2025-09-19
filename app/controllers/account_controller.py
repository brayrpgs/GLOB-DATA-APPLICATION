from typing import Optional
from fastapi import HTTPException
from asyncpg import Pool
from app.repository.account_repository import AccountRepository
import logging

logger = logging.getLogger(__name__)

async def post_account_controller(
    db_pool: Pool,
    email: str,
    username: str,
    hashed_password: str,
    avatar_url: str,
    status: int
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = AccountRepository(db_pool)
    try:
        return await repo.post_account(email, username, hashed_password, avatar_url, status)
    except Exception as e:
        logger.exception("Error en post_account_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def get_account_controller(
    db_pool: Pool,
    user_id: Optional[int] = None,
    email: Optional[str] = None,
    username: Optional[str] = None,
    status: Optional[int] = None,
    membership_plan_id: Optional[int] = None,
    page: int = 1,
    limit: int = 10
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = AccountRepository(db_pool)
    try:
        data = await repo.get_account(user_id, email, username, status, membership_plan_id, page, limit)
        return {"data": data, "page": page, "currentLimit": limit, "totalData": len(data) if data else 0}
    except Exception as e:
        logger.exception("Error en get_account_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def patch_account_controller(
    db_pool: Pool,
    user_id: int,
    email: Optional[str] = None,
    username: Optional[str] = None,
    hashed_password: Optional[str] = None,
    avatar_url: Optional[str] = None,
    status: Optional[int] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = AccountRepository(db_pool)
    try:
        return await repo.patch_account(user_id, email, username, hashed_password, avatar_url, status)
    except Exception as e:
        logger.exception("Error en patch_account_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def put_account_controller(
    db_pool: Pool,
    user_id: int,
    email: str,
    username: str,
    hashed_password: str,
    avatar_url: str,
    status: int
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = AccountRepository(db_pool)
    try:
        return await repo.put_account(user_id, email, username, hashed_password, avatar_url, status)
    except Exception as e:
        logger.exception("Error en put_account_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def delete_account_controller(db_pool: Pool, user_id: int) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = AccountRepository(db_pool)
    try:
        success = await repo.delete_account(user_id)
        return {"success": success, "message": "Account deleted successfully" if success else "Failed to delete account"}
    except Exception as e:
        logger.exception("Error en delete_account_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))