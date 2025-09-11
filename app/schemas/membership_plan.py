from pydantic import BaseModel
from typing import Optional

class MembershipPlanSchema(BaseModel):
    membershipplan_id: int
    name: str
    description: Optional[str] = None
    amount: Optional[float] = None

    class Config:
        orm_mode = True

class MembershipPlanCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    amount: Optional[float] = None
