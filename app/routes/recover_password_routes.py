from fastapi import APIRouter, Query, Depends
from asyncpg import Pool
from app.controllers.recover_password_controller import (
    post_recover_password_controller,
    get_recover_password_controller,
    patch_recover_password_controller,
    put_recover_password_controller,
    delete_recover_password_controller
)
from app.database.conection import get_pool
from datetime import date
from typing import Optional

router = APIRouter(
    prefix="/recover-passwords",
    tags=["recover-passwords"]
)

@router.post("/")
async def create_recover_password(
    user_id: int = Query(...),
    otp: str = Query(...),
    is_used: int = Query(...),
    expiry_date: date = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await post_recover_password_controller(db_pool, user_id, otp, is_used, expiry_date)

@router.get("/")
async def get_recover_passwords(
    recover_password_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    otp: Optional[str] = Query(None),
    is_used: Optional[int] = Query(None),
    expiry_date: Optional[date] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool)
):
    return await get_recover_password_controller(db_pool, recover_password_id, user_id, otp, is_used, expiry_date, page, limit)

@router.patch("/")
async def patch_recover_password(
    recover_password_id: int = Query(...),
    user_id: Optional[int] = Query(None),
    otp: Optional[str] = Query(None),
    is_used: Optional[int] = Query(None),
    expiry_date: Optional[date] = Query(None),
    db_pool: Pool = Depends(get_pool)
):
    return await patch_recover_password_controller(db_pool, recover_password_id, user_id, otp, is_used, expiry_date)

@router.put("/")
async def put_recover_password(
    recover_password_id: int = Query(...),
    user_id: int = Query(...),
    otp: str = Query(...),
    is_used: int = Query(...),
    expiry_date: date = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await put_recover_password_controller(db_pool, recover_password_id, user_id, otp, is_used, expiry_date)

@router.delete("/{recover_password_id}")
async def delete_recover_password(recover_password_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_recover_password_controller(db_pool, recover_password_id)