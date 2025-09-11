from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class PaymentInfoSchema(BaseModel):
    payment_info_id: int
    user_id: int
    method: int
    last_four_digits: Optional[str] = None
    status: Optional[int] = None
    next_payment_date: Optional[date] = None
    audit_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class PaymentInfoCreateSchema(BaseModel):
    user_id: int
    method: int
    last_four_digits: Optional[str] = None
    status: Optional[int] = None
    next_payment_date: Optional[date] = None
    audit_id: int
