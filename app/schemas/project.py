from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class ProjectSchema(BaseModel):
    project_id: int
    name: str
    description: Optional[str] = None
    user_project_id_fk: Optional[int] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None
    status: Optional[int] = None
    progress: Optional[Decimal] = None

    class Config:
        orm_mode = True

class ProjectCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    user_project_id_fk: Optional[int] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None
    status: Optional[int] = None
    progress: Optional[Decimal] = None
