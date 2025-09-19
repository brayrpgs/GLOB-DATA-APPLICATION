from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class IssueTypeBase(BaseModel):
    status: Optional[int] = None
    priority: Optional[int] = None

class IssueTypeCreate(IssueTypeBase):
    pass

class IssueTypePatch(IssueTypeBase):
    issue_type_id: int

class IssueTypePut(IssueTypeBase):
    issue_type_id: int

class IssueTypeResponse(BaseModel):
    data: List[Dict[str, Any]]
    page: int
    currentLimit: int
    totalData: int
