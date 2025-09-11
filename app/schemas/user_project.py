from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class UserProjectSchema(BaseModel):
    user_project_id: int
    user_id_fk: int
    rol_proyect: Optional[int] = None
    productivity: Optional[Decimal] = None

    class Config:
        orm_mode = True

class UserProjectCreateSchema(BaseModel):
    user_id_fk: int
    rol_proyect: Optional[int] = None
    productivity: Optional[Decimal] = None
