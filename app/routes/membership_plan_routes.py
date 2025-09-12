from fastapi import APIRouter, Query, Body, status
from typing import List, Optional
from app.schemas.membership_plan import MembershipPlanSchema, MembershipPlanCreateSchema
from app.controllers.membership_plan_controller import (
    get_membership_plans,
    create_membership_plan,
    put_membership_plan,
    patch_membership_plan,
    delete_membership_plan,
)

router = APIRouter(prefix="/membership-plans", tags=["Membership Plans"])

@router.get("/", response_model=List[MembershipPlanSchema])
def route_get_membership_plans(
    membershipplan_id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    amount: Optional[float] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    return get_membership_plans(membershipplan_id, name, description, amount, page, limit)

@router.post("/", response_model=MembershipPlanSchema, status_code=status.HTTP_201_CREATED)
def route_create_membership_plan(plan: MembershipPlanCreateSchema = Body(...)):
    return create_membership_plan(plan)

@router.put("/{membershipplan_id}", response_model=MembershipPlanSchema)
def route_put_membership_plan(membershipplan_id: int, plan: MembershipPlanCreateSchema = Body(...)):
    return put_membership_plan(membershipplan_id, plan)

@router.patch("/{membershipplan_id}", response_model=MembershipPlanSchema)
def route_patch_membership_plan(membershipplan_id: int, plan: MembershipPlanCreateSchema = Body(...)):
    return patch_membership_plan(membershipplan_id, plan)

@router.delete("/{membershipplan_id}", response_model=dict)
def route_delete_membership_plan(membershipplan_id: int):
    return delete_membership_plan(membershipplan_id)
