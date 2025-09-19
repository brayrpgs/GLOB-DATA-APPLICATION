from typing import Optional
from fastapi import HTTPException
from asyncpg import Pool
from app.repository.recover_password_repository import RecoverPasswordRepository
import logging
from datetime import date

logger = logging.getLogger(__name__)

async def post_recover_password_controller(
    db_pool: Pool,
    user_id: int,
    otp: str,
    is_used: int,
    expiry_date: date
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = RecoverPasswordRepository(db_pool)
    try:
        return await repo.post_recover_password(user_id, otp, is_used, expiry_date)
    except Exception as e:
        logger.exception("Error en post_recover_password_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def get_recover_password_controller(
    db_pool: Pool,
    recover_password_id: Optional[int] = None,
    user_id: Optional[int] = None,
    otp: Optional[str] = None,
    is_used: Optional[int] = None,
    expiry_date: Optional[date] = None,
    page: int = 1,
    limit: int = 10
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = RecoverPasswordRepository(db_pool)
    try:
        data = await repo.get_recover_password(recover_password_id, user_id, otp, is_used, expiry_date, page, limit)
        return {"data": data, "page": page, "currentLimit": limit, "totalData": len(data) if data else 0}
    except Exception as e:
        logger.exception("Error en get_recover_password_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def patch_recover_password_controller(
    db_pool: Pool,
    recover_password_id: int,
    user_id: Optional[int] = None,
    otp: Optional[str] = None,
    is_used: Optional[int] = None,
    expiry_date: Optional[date] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = RecoverPasswordRepository(db_pool)
    try:
        return await repo.patch_recover_password(recover_password_id, user_id, otp, is_used, expiry_date)
    except Exception as e:
        logger.exception("Error en patch_recover_password_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def put_recover_password_controller(
    db_pool: Pool,
    recover_password_id: int,
    user_id: int,
    otp: str,
    is_used: int,
    expiry_date: date
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = RecoverPasswordRepository(db_pool)
    try:
        return await repo.put_recover_password(recover_password_id, user_id, otp, is_used, expiry_date)
    except Exception as e:
        logger.exception("Error en put_recover_password_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def delete_recover_password_controller(db_pool: Pool, recover_password_id: int) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = RecoverPasswordRepository(db_pool)
    try:
        return await repo.delete_recover_password(recover_password_id)
    except Exception as e:
        logger.exception("Error en delete_recover_password_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))