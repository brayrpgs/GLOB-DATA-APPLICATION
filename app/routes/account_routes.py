from fastapi import APIRouter, Query, Depends
from asyncpg import Pool
from app.controllers.account_controller import (
    post_account_controller,
    get_account_controller,
    patch_account_controller,
    put_account_controller,
    delete_account_controller
)
from app.database.conection import get_pool
from typing import Optional

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"]
)

@router.post("/")
async def create_account(
    email: str = Query(...),
    username: str = Query(...),
    hashed_password: str = Query(...),
    avatar_url: str = Query(...),
    status: int = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await post_account_controller(db_pool, email, username, hashed_password, avatar_url, status)

@router.get("/")
async def get_accounts(
    user_id: Optional[int] = Query(None),
    email: Optional[str] = Query(None),
    username: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    membership_plan_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool)
):
    return await get_account_controller(db_pool, user_id, email, username, status, membership_plan_id, page, limit)

@router.patch("/")
async def patch_account(
    user_id: int = Query(...),
    email: Optional[str] = Query(None),
    username: Optional[str] = Query(None),
    hashed_password: Optional[str] = Query(None),
    avatar_url: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    db_pool: Pool = Depends(get_pool)
):
    return await patch_account_controller(db_pool, user_id, email, username, hashed_password, avatar_url, status)

@router.put("/")
async def put_account(
    user_id: int = Query(...),
    email: str = Query(...),
    username: str = Query(...),
    hashed_password: str = Query(...),
    avatar_url: str = Query(...),
    status: int = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await put_account_controller(db_pool, user_id, email, username, hashed_password, avatar_url, status)

@router.delete("/{user_id}")
async def delete_account(user_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_account_controller(db_pool, user_id)