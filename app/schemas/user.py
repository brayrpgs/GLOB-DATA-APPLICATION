from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class MembershipPlanSchema(BaseModel):
    membershipplan_id: int
    name: str
    description: Optional[str] = None
    amount: Optional[float] = None

    class Config:
        orm_mode = True

class AuditSchema(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    user_id: int
    audit_id: Optional[int]
    email: EmailStr
    username: str
    hashed_password: str
    avatar_url: Optional[str] = None
    status: Optional[int]
    membership_plan: Optional[MembershipPlanSchema]
    user_created_at: Optional[datetime]
    user_updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class UserCreateSchema(BaseModel):
    email: EmailStr
    username: str
    hashed_password: str
    avatar_url: Optional[str] = None
    status: Optional[int]
    membership_plan_id: Optional[int]
