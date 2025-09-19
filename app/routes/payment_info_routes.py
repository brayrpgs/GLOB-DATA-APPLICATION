from fastapi import APIRouter, Query, Depends
from asyncpg import Pool
from app.controllers.payment_info_controller import (
    post_payment_info_controller,
    get_payment_info_controller,
    patch_payment_info_controller,
    put_payment_info_controller,
    delete_payment_info_controller
)
from app.database.conection import get_pool
from datetime import date
from typing import Optional

router = APIRouter(
    prefix="/payment-info",
    tags=["payment-info"]
)

@router.post("/")
async def create_payment_info(
    user_id: int = Query(...),
    method: int = Query(...),
    last_four_digits: str = Query(...),
    status: int = Query(...),
    next_payment_date: date = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await post_payment_info_controller(db_pool, user_id, method, last_four_digits, status, next_payment_date)

@router.get("/")
async def get_payment_info(
    payment_info_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    method: Optional[int] = Query(None),
    status: Optional[int] = Query(None),
    next_payment_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool)
):
    return await get_payment_info_controller(db_pool, payment_info_id, user_id, method, status, next_payment_date, page, limit)

@router.patch("/")
async def patch_payment_info(
    payment_info_id: int = Query(...),
    user_id: Optional[int] = Query(None),
    method: Optional[int] = Query(None),
    last_four_digits: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    next_payment_date: Optional[date] = Query(None),
    db_pool: Pool = Depends(get_pool)
):
    return await patch_payment_info_controller(db_pool, payment_info_id, user_id, method, last_four_digits, status, next_payment_date)

@router.put("/")
async def put_payment_info(
    payment_info_id: int = Query(...),
    user_id: int = Query(...),
    method: int = Query(...),
    last_four_digits: str = Query(...),
    status: int = Query(...),
    next_payment_date: date = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await put_payment_info_controller(db_pool, payment_info_id, user_id, method, last_four_digits, status, next_payment_date)

@router.delete("/{payment_info_id}")
async def delete_payment_info(payment_info_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_payment_info_controller(db_pool, payment_info_id)