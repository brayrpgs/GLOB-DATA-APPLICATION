from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from decimal import Decimal

class MembershipPlanBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = None

class MembershipPlanCreate(BaseModel):
    name: str
    description: str
    amount: Decimal

class MembershipPlanPatch(BaseModel):
    membershipplan_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = None

class MembershipPlanPut(BaseModel):
    membershipplan_id: int
    name: str
    description: str
    amount: Decimal

class MembershipPlanResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: int
    currentLimit: int
    totalData: int

class MembershipPlanDeleteResponse(BaseModel):
    success: bool
    message: str