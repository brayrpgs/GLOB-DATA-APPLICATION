from pydantic import BaseModel
from typing import Optional
from datetime import date

class SprintSchema(BaseModel):
    sprint_id: int
    name: str
    description: Optional[str] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None

    class Config:
        orm_mode = True

class SprintCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None
