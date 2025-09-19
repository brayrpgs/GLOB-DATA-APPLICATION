from typing import Optional
from fastapi import HTTPException
from asyncpg import Pool
from app.repository.membership_plan import MembershipPlanRepository
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

async def post_membership_plan_controller(
    db_pool: Pool,
    name: str,
    description: str,
    amount: Decimal
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = MembershipPlanRepository(db_pool)
    try:
        return await repo.post_membership_plan(name, description, amount)
    except Exception as e:
        logger.exception("Error en post_membership_plan_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def get_membership_plan_controller(
    db_pool: Pool,
    membershipplan_id: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    amount: Optional[Decimal] = None,
    page: int = 1,
    limit: int = 10
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = MembershipPlanRepository(db_pool)
    try:
        data = await repo.get_membership_plan(membershipplan_id, name, description, amount, page, limit)
        return {"data": data, "page": page, "currentLimit": limit, "totalData": len(data) if data else 0}
    except Exception as e:
        logger.exception("Error en get_membership_plan_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def patch_membership_plan_controller(
    db_pool: Pool,
    membershipplan_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    amount: Optional[Decimal] = None
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = MembershipPlanRepository(db_pool)
    try:
        return await repo.patch_membership_plan(membershipplan_id, name, description, amount)
    except Exception as e:
        logger.exception("Error en patch_membership_plan_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def put_membership_plan_controller(
    db_pool: Pool,
    membershipplan_id: int,
    name: str,
    description: str,
    amount: Decimal
) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = MembershipPlanRepository(db_pool)
    try:
        return await repo.put_membership_plan(membershipplan_id, name, description, amount)
    except Exception as e:
        logger.exception("Error en put_membership_plan_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

async def delete_membership_plan_controller(db_pool: Pool, membershipplan_id: int) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no disponible")
    repo = MembershipPlanRepository(db_pool)
    try:
        success = await repo.delete_membership_plan(membershipplan_id)
        return {"success": success, "message": "Membership plan deleted successfully" if success else "Failed to delete membership plan"}
    except Exception as e:
        logger.exception("Error en delete_membership_plan_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))