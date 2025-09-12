from fastapi import APIRouter
from typing import List
from app.schemas.issue import IssueSchema, IssueCreateSchema
from app.controllers.issue_controller import create_issue, get_issues, patch_issue, put_issue, delete_issue

router = APIRouter(prefix="/issues", tags=["Issues"])

@router.post("/", response_model=IssueSchema)
def post_issue(issue: IssueCreateSchema):
    return create_issue(issue)

@router.get("/", response_model=List[IssueSchema])
def list_issues(
    issue_id: int = None,
    summary: str = None,
    description: str = None,
    audit_id: int = None,
    resolve_at: str = None,
    due_date: str = None,
    votes: int = None,
    original_estimation: int = None,
    custom_start_date: str = None,
    story_point_estimate: int = None,
    parent_summary: int = None,
    issue_type: int = None,
    project_id_fk: int = None,
    user_assigned_fk: int = None,
    user_creator_issue_fk: int = None,
    user_informator_fk: int = None,
    sprint_id_fk: int = None,
    status_issue: int = None,
    page: int = 1,
    limit: int = 10
):
    return get_issues(
        issue_id,
        summary,
        description,
        audit_id,
        resolve_at,
        due_date,
        votes,
        original_estimation,
        custom_start_date,
        story_point_estimate,
        parent_summary,
        issue_type,
        project_id_fk,
        user_assigned_fk,
        user_creator_issue_fk,
        user_informator_fk,
        sprint_id_fk,
        status_issue,
        page,
        limit
    )

@router.patch("/{issue_id}", response_model=IssueSchema)
def patch_issue_route(issue_id: int, issue: IssueCreateSchema):
    return patch_issue(issue_id, issue)

@router.put("/{issue_id}", response_model=IssueSchema)
def put_issue_route(issue_id: int, issue: IssueCreateSchema):
    return put_issue(issue_id, issue)

@router.delete("/{issue_id}", response_model=IssueSchema)
def delete_issue_route(issue_id: int):
    return delete_issue(issue_id)
