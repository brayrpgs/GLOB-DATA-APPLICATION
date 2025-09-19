from fastapi import APIRouter, Query, Depends
from asyncpg import Pool
from app.controllers.membership_plan_controller import (
    post_membership_plan_controller,
    get_membership_plan_controller,
    patch_membership_plan_controller,
    put_membership_plan_controller,
    delete_membership_plan_controller
)
from app.database.conection import get_pool
from decimal import Decimal
from typing import Optional

router = APIRouter(
    prefix="/membership-plans",
    tags=["membership-plans"]
)

@router.post("/")
async def create_membership_plan(
    name: str = Query(...),
    description: str = Query(...),
    amount: Decimal = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await post_membership_plan_controller(db_pool, name, description, amount)

@router.get("/")
async def get_membership_plans(
    membershipplan_id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    amount: Optional[Decimal] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool)
):
    return await get_membership_plan_controller(db_pool, membershipplan_id, name, description, amount, page, limit)

@router.patch("/")
async def patch_membership_plan(
    membershipplan_id: int = Query(...),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    amount: Optional[Decimal] = Query(None),
    db_pool: Pool = Depends(get_pool)
):
    return await patch_membership_plan_controller(db_pool, membershipplan_id, name, description, amount)

@router.put("/")
async def put_membership_plan(
    membershipplan_id: int = Query(...),
    name: str = Query(...),
    description: str = Query(...),
    amount: Decimal = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await put_membership_plan_controller(db_pool, membershipplan_id, name, description, amount)

@router.delete("/{membershipplan_id}")
async def delete_membership_plan(membershipplan_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_membership_plan_controller(db_pool, membershipplan_id)