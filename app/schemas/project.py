from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    user_project_id_fk: Optional[int] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None
    status: Optional[int] = None
    progress: Optional[Decimal] = None

class ProjectCreate(BaseModel):
    name: str
    description: str
    user_project_id_fk: int
    date_init: date
    date_end: date
    status: int
    progress: Decimal

class ProjectPatch(BaseModel):
    project_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    user_project_id_fk: Optional[int] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None
    status: Optional[int] = None
    progress: Optional[Decimal] = None

class ProjectPut(BaseModel):
    project_id: int
    name: str
    description: str
    user_project_id_fk: int
    date_init: date
    date_end: date
    status: int
    progress: Decimal

class ProjectResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: int
    currentLimit: int
    totalData: int