from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import date

class RecoverPasswordBase(BaseModel):
    user_id: Optional[int] = None
    otp: Optional[str] = None
    is_used: Optional[int] = None
    expiry_date: Optional[date] = None

class RecoverPasswordCreate(BaseModel):
    user_id: int
    otp: str
    is_used: int
    expiry_date: date

class RecoverPasswordPatch(BaseModel):
    recover_password_id: int
    user_id: Optional[int] = None
    otp: Optional[str] = None
    is_used: Optional[int] = None
    expiry_date: Optional[date] = None

class RecoverPasswordPut(BaseModel):
    recover_password_id: int
    user_id: int
    otp: str
    is_used: int
    expiry_date: date

class RecoverPasswordResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: int
    currentLimit: int
    totalData: int