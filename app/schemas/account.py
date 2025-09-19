from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class AccountBase(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    avatar_url: Optional[str] = None
    status: Optional[int] = None

class AccountCreate(BaseModel):
    email: str
    username: str
    hashed_password: str
    avatar_url: str
    status: int

class AccountPatch(BaseModel):
    user_id: int
    email: Optional[str] = None
    username: Optional[str] = None
    hashed_password: Optional[str] = None
    avatar_url: Optional[str] = None
    status: Optional[int] = None

class AccountPut(BaseModel):
    user_id: int
    email: str
    username: str
    hashed_password: str
    avatar_url: str
    status: int

class AccountWithDetails(BaseModel):
    user_id: int
    audit_id: int
    email: str
    username: str
    hashed_password: str
    avatar_url: str
    status: int
    membershipplan_id: Optional[int] = None
    membership_plan_name: Optional[str] = None
    membership_plan_description: Optional[str] = None
    membership_plan_amount: Optional[Decimal] = None
    user_created_at: datetime
    user_updated_at: datetime

class AccountResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: int
    currentLimit: int
    totalData: int

class AccountDeleteResponse(BaseModel):
    success: bool
    message: str