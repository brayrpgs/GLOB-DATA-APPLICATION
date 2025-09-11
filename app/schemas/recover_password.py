from pydantic import BaseModel
from typing import Optional
from datetime import date

class RecoverPasswordSchema(BaseModel):
    recover_password_id: int
    user_id: int
    otp: str
    is_used: Optional[bool] = False
    expiry_date: date

    class Config:
        orm_mode = True

class RecoverPasswordCreateSchema(BaseModel):
    user_id: int
    otp: str
    expiry_date: date
    is_used: Optional[bool] = False
