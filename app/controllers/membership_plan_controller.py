from typing import List, Optional
from fastapi import HTTPException
from app.database.conection import get_connection
from app.schemas.membership_plan import MembershipPlanSchema, MembershipPlanCreateSchema

def get_membership_plans(
    membershipplan_id: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    amount: Optional[float] = None,
    page: int = 1,
    limit: int = 10,
) -> List[MembershipPlanSchema]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("GET_MEMBERSHIP_PLAN", [membershipplan_id, name, description, amount, page, limit])
            result = cur.fetchone()
            return result["data"] if result and "data" in result else []

def create_membership_plan(plan: MembershipPlanCreateSchema) -> MembershipPlanSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("POST_MEMBERSHIP_PLAN", [plan.name, plan.description, plan.amount])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=500, detail="MembershipPlan could not be created")
            return result["data"][0] if isinstance(result["data"], list) else result["data"]

def put_membership_plan(membershipplan_id: int, plan: MembershipPlanCreateSchema) -> MembershipPlanSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("PUT_MEMBERSHIP_PLAN", [membershipplan_id, plan.name, plan.description, plan.amount])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"MembershipPlan with ID {membershipplan_id} not found")
            return result["data"][0] if isinstance(result["data"], list) else result["data"]

def patch_membership_plan(membershipplan_id: int, plan: MembershipPlanCreateSchema) -> MembershipPlanSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("PATCH_MEMBERSHIP_PLAN", [membershipplan_id, plan.name, plan.description, plan.amount])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"MembershipPlan with ID {membershipplan_id} not found")
            return result["data"][0] if isinstance(result["data"], list) else result["data"]

def delete_membership_plan(membershipplan_id: int) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("DELETE_MEMBERSHIP_PLAN", [membershipplan_id])
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail=f"MembershipPlan with ID {membershipplan_id} not found")
            # DELETE returns only success status, not full object
            return {"membershipplan_id": membershipplan_id, "deleted": True}
