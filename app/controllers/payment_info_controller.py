from typing import Optional
from fastapi import HTTPException
from asyncpg import Pool
from app.repository.payment_info_repository import PaymentInfoRepository
import logging
from datetime import date

logger = logging.getLogger(__name__)

async def post_payment_info_controller(
    db_pool: Pool,
    user_id: int,
    method: int,
    last_four_digits: str,
    status: int,
    next_payment_date: date
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = PaymentInfoRepository(db_pool)
    try:
        return await repo.post_payment_info(user_id, method, last_four_digits, status, next_payment_date)
    except Exception as e:
        logger.exception("Error en post_payment_info_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def get_payment_info_controller(
    db_pool: Pool,
    payment_info_id: Optional[int] = None,
    user_id: Optional[int] = None,
    method: Optional[int] = None,
    status: Optional[int] = None,
    next_payment_date: Optional[date] = None,
    page: int = 1,
    limit: int = 10
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = PaymentInfoRepository(db_pool)
    try:
        data = await repo.get_payment_info(payment_info_id, user_id, method, status, next_payment_date, page, limit)
        return {"data": data, "page": page, "currentLimit": limit, "totalData": len(data) if data else 0}
    except Exception as e:
        logger.exception("Error en get_payment_info_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def patch_payment_info_controller(
    db_pool: Pool,
    payment_info_id: int,
    user_id: Optional[int] = None,
    method: Optional[int] = None,
    last_four_digits: Optional[str] = None,
    status: Optional[int] = None,
    next_payment_date: Optional[date] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = PaymentInfoRepository(db_pool)
    try:
        return await repo.patch_payment_info(payment_info_id, user_id, method, last_four_digits, status, next_payment_date)
    except Exception as e:
        logger.exception("Error en patch_payment_info_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def put_payment_info_controller(
    db_pool: Pool,
    payment_info_id: int,
    user_id: int,
    method: int,
    last_four_digits: str,
    status: int,
    next_payment_date: date
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = PaymentInfoRepository(db_pool)
    try:
        return await repo.put_payment_info(payment_info_id, user_id, method, last_four_digits, status, next_payment_date)
    except Exception as e:
        logger.exception("Error en put_payment_info_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def delete_payment_info_controller(db_pool: Pool, payment_info_id: int) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = PaymentInfoRepository(db_pool)
    try:
        return await repo.delete_payment_info(payment_info_id)
    except Exception as e:
        logger.exception("Error en delete_payment_info_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))