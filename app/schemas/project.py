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
    # Make fields optional so route returns 400 instead of 422 on missing fields
    name: Optional[str] = None
    description: Optional[str] = None
    user_project_id_fk: Optional[int] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None
    status: Optional[int] = None
    progress: Optional[Decimal] = None

class ProjectPatch(BaseModel):
    # project_id must be provided in the path, not the body
    name: Optional[str] = None
    description: Optional[str] = None
    user_project_id_fk: Optional[int] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None
    status: Optional[int] = None
    progress: Optional[Decimal] = None

class ProjectPut(BaseModel):
    # project_id must be provided in the path, not the body
    # Make fields optional so route validates and returns 400 instead of 422
    name: Optional[str] = None
    description: Optional[str] = None
    user_project_id_fk: Optional[int] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None
    status: Optional[int] = None
    progress: Optional[Decimal] = None

class ProjectResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: int
    currentLimit: int
    totalData: int