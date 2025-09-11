from pydantic import BaseModel
from typing import Optional
from datetime import date

class IssueSchema(BaseModel):
    issue_id: int
    summary: str
    description: Optional[str] = None
    audit_id_fk: Optional[int] = None
    resolve_at: Optional[date] = None
    due_date: Optional[date] = None
    votes: Optional[int] = None
    original_estimation: Optional[int] = None
    custom_start_date: Optional[date] = None
    story_point_estimate: Optional[int] = None
    parent_summary_fk: Optional[int] = None
    issue_type: Optional[int] = None
    project_id_fk: Optional[int] = None
    user_assigned_fk: Optional[int] = None
    user_creator_issue_fk: Optional[int] = None
    user_informator_fk: Optional[int] = None
    sprint_id_fk: Optional[int] = None
    status_issue: Optional[int] = None

    class Config:
        orm_mode = True

class IssueCreateSchema(BaseModel):
    summary: str
    description: Optional[str] = None
    audit_id_fk: Optional[int] = None
    resolve_at: Optional[date] = None
    due_date: Optional[date] = None
    votes: Optional[int] = None
    original_estimation: Optional[int] = None
    custom_start_date: Optional[date] = None
    story_point_estimate: Optional[int] = None
    parent_summary_fk: Optional[int] = None
    issue_type: Optional[int] = None
    project_id_fk: Optional[int] = None
    user_assigned_fk: Optional[int] = None
    user_creator_issue_fk: Optional[int] = None
    user_informator_fk: Optional[int] = None
    sprint_id_fk: Optional[int] = None
    status_issue: Optional[int] = None
