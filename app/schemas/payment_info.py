from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import date, datetime

class PaymentInfoBase(BaseModel):
    user_id: Optional[int] = None
    method: Optional[int] = None
    last_four_digits: Optional[str] = None
    status: Optional[int] = None
    next_payment_date: Optional[date] = None

class PaymentInfoCreate(BaseModel):
    user_id: int
    method: int
    last_four_digits: str
    status: int
    next_payment_date: date

class PaymentInfoPatch(BaseModel):
    payment_info_id: int
    user_id: Optional[int] = None
    method: Optional[int] = None
    last_four_digits: Optional[str] = None
    status: Optional[int] = None
    next_payment_date: Optional[date] = None

class PaymentInfoPut(BaseModel):
    payment_info_id: int
    user_id: int
    method: int
    last_four_digits: str
    status: int
    next_payment_date: date

class PaymentInfoWithAudit(BaseModel):
    payment_info_id: int
    user_id: int
    method: int
    last_four_digits: str
    status: int
    next_payment_date: date
    audit_id: int
    created_at: datetime
    updated_at: datetime

class PaymentInfoResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: int
    currentLimit: int
    totalData: int