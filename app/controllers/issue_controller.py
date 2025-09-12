# controllers/issue_controller.py
from app.database.conection import get_connection
from app.schemas.issue import IssueSchema, IssueCreateSchema
from fastapi import HTTPException
from typing import List, Optional

def create_issue(issue: IssueCreateSchema) -> IssueSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "POST_ISSUE",
                [
                    issue.summary,
                    issue.description,
                    issue.resolve_at,
                    issue.due_date,
                    issue.votes,
                    issue.original_estimation,
                    issue.custom_start_date,
                    issue.story_point_estimate,
                    issue.parent_summary_fk,
                    issue.issue_type,
                    issue.project_id_fk,
                    issue.user_assigned_fk,
                    issue.user_creator_issue_fk,
                    issue.user_informator_fk,
                    issue.sprint_id_fk,
                    issue.status_issue,
                ],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(
                    status_code=500,
                    detail="Issue could not be created"
                )
            return result["data"]


def get_issues(
    issue_id: Optional[int] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    audit_id: Optional[int] = None,
    resolve_at: Optional[str] = None,
    due_date: Optional[str] = None,
    votes: Optional[int] = None,
    original_estimation: Optional[int] = None,
    custom_start_date: Optional[str] = None,
    story_point_estimate: Optional[int] = None,
    parent_summary: Optional[int] = None,
    issue_type: Optional[int] = None,
    project_id_fk: Optional[int] = None,
    user_assigned_fk: Optional[int] = None,
    user_creator_issue_fk: Optional[int] = None,
    user_informator_fk: Optional[int] = None,
    sprint_id_fk: Optional[int] = None,
    status_issue: Optional[int] = None,
    page: int = 1,
    limit: int = 10,
) -> List[IssueSchema]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "GET_ISSUE",
                [
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
                ]
            )
            result = cur.fetchone()
            return result["data"] if result and "data" in result else []


def patch_issue(issue_id: int, issue: IssueCreateSchema) -> IssueSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PATCH_ISSUE",
                [
                    issue_id,
                    issue.summary,
                    issue.description,
                    issue.audit_id_fk,
                    issue.resolve_at,
                    issue.due_date,
                    issue.votes,
                    issue.original_estimation,
                    issue.custom_start_date,
                    issue.story_point_estimate,
                    issue.parent_summary_fk,
                    issue.issue_type,
                    issue.project_id_fk,
                    issue.user_assigned_fk,
                    issue.user_creator_issue_fk,
                    issue.user_informator_fk,
                    issue.sprint_id_fk,
                    issue.status_issue,
                ],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(
                    status_code=404,
                    detail=f"Issue with ID {issue_id} not found"
                )
            return result["data"]


def put_issue(issue_id: int, issue: IssueCreateSchema) -> IssueSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PUT_ISSUE",
                [
                    issue_id,
                    issue.summary,
                    issue.description,
                    issue.audit_id_fk,
                    issue.resolve_at,
                    issue.due_date,
                    issue.votes,
                    issue.original_estimation,
                    issue.custom_start_date,
                    issue.story_point_estimate,
                    issue.parent_summary_fk,
                    issue.issue_type,
                    issue.project_id_fk,
                    issue.user_assigned_fk,
                    issue.user_creator_issue_fk,
                    issue.user_informator_fk,
                    issue.sprint_id_fk,
                    issue.status_issue,
                ],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(
                    status_code=404,
                    detail=f"Issue with ID {issue_id} not found"
                )
            # GET_ISSUE returns a list, pick first
            return result["data"][0] if isinstance(result["data"], list) else result["data"]


def delete_issue(issue_id: int) -> IssueSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("DELETE_ISSUE", [issue_id])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(
                    status_code=404,
                    detail=f"Issue with ID {issue_id} not found"
                )
            return result["data"]
