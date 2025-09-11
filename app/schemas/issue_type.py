from pydantic import BaseModel
from typing import Optional

class IssueTypeSchema(BaseModel):
    issue_type_id: int
    status: Optional[int] = None
    priority: Optional[int] = None

    class Config:
        orm_mode = True

class IssueTypeCreateSchema(BaseModel):
    status: Optional[int] = None
    priority: Optional[int] = None
