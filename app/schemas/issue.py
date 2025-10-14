from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import date


class IssueBase(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    audit_id: Optional[int] = None
    resolve_at: Optional[date] = None
    due_date: Optional[date] = None
    votes: Optional[int] = None
    original_estimation: Optional[int] = None
    custom_start_date: Optional[date] = None
    story_point_estimate: Optional[int] = None
    parent_summary: Optional[int] = None
    issue_type: Optional[int] = None
    project_id: Optional[int] = None
    user_assigned: Optional[int] = None
    user_creator: Optional[int] = None
    user_informator: Optional[int] = None
    sprint_id: Optional[int] = None
    status: Optional[int] = None


class IssueCreate(BaseModel):
    """Schema for creating a new issue. All required fields must be provided."""
    summary: str
    description: str
    resolve_at: date
    due_date: date
    votes: int
    original_estimation: int
    custom_start_date: date
    story_point_estimate: int
    parent_summary: Optional[int] = None
    issue_type: int
    project_id: Optional[int] = None
    user_assigned: Optional[int] = None
    user_creator: Optional[int] = None
    user_informator: Optional[int] = None
    sprint_id: Optional[int] = None
    status: int


class IssuePatchRequest(IssueBase):
    """Schema for partial update (PATCH). All fields are optional."""
    pass


class IssuePutRequest(BaseModel):
    """Schema for full replacement (PUT). All required fields must be provided."""
    summary: str
    description: str
    audit_id: int
    resolve_at: date
    due_date: date
    votes: int
    original_estimation: int
    custom_start_date: date
    story_point_estimate: int
    parent_summary: Optional[int] = None
    issue_type: int
    project_id: Optional[int] = None
    user_assigned: Optional[int] = None
    user_creator: Optional[int] = None
    user_informator: Optional[int] = None
    sprint_id: Optional[int] = None
    status: int


class IssueResponse(BaseModel):
    """Response model for issue queries."""
    Issues: List[Dict[str, Any]]
    page: int
    currentLimit: int
    totalData: int