from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from decimal import Decimal

class UserProjectBase(BaseModel):
    user_id_fk: Optional[int] = None
    rol_proyect: Optional[int] = None
    productivity: Optional[Decimal] = None

class UserProjectCreate(BaseModel):
    user_id_fk: int
    rol_proyect: int
    productivity: Decimal

class UserProjectPatch(BaseModel):
    user_id_fk: Optional[int] = None
    rol_proyect: Optional[int] = None
    productivity: Optional[Decimal] = None

class UserProjectPut(BaseModel):
    user_id_fk: int
    rol_proyect: int
    productivity: Decimal

class UserProjectResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: int
    currentLimit: int
    totalData: int