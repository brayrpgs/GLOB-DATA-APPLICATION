from datetime import date
from typing import Optional
from fastapi import APIRouter, Query, HTTPException,Depends
from asyncpg import Pool
from app.controllers.issue_controller import get_issues_controller,delete_issue_controller,post_issue_controller
from app.schemas.issue import IssueResponse,IssueCreate
from app.database.conection import get_pool

router = APIRouter(
    prefix="/issues",
    tags=["issues"]
)

@router.post("/")
async def create_issue(
    summary: str = Query(...),
    description: str = Query(...),
    resolve_at: date = Query(...),
    due_date: date = Query(...),
    votes: int = Query(...),
    original_estimation: int = Query(...),
    custom_start_date: date = Query(...),
    story_point_estimate: int = Query(...),
    parent_summary: Optional[int] = Query(None),
    issue_type: int = Query(...),
    project_id: int = Query(...),
    user_assigned: int = Query(...),
    user_creator: int = Query(...),
    user_informator: int = Query(...),
    sprint_id: int = Query(...),
    status: int = Query(...),
):
    pool: Pool = get_pool()
    issue_data = {
        "summary": summary,
        "description": description,
        "resolve_at": resolve_at,
        "due_date": due_date,
        "votes": votes,
        "original_estimation": original_estimation,
        "custom_start_date": custom_start_date,
        "story_point_estimate": story_point_estimate,
        "parent_summary": parent_summary,
        "issue_type": issue_type,
        "project_id": project_id,
        "user_assigned": user_assigned,
        "user_creator": user_creator,
        "user_informator": user_informator,
        "sprint_id": sprint_id,
        "status": status,
    }
    return await post_issue_controller(pool, issue_data)

@router.get("/", response_model=IssueResponse)
async def get_issues(
    issue_id: int = Query(None),
    summary: str = Query(None),
    description: str = Query(None),
    audit_id: int = Query(None),
    resolve_at: str = Query(None),
    due_date: str = Query(None),
    votes: int = Query(None),
    original_estimation: int = Query(None),
    custom_start_date: str = Query(None),
    story_point_estimate: int = Query(None),
    parent_summary: int = Query(None),
    issue_type: int = Query(None),
    project_id_fk: int = Query(None),
    user_assigned_fk: int = Query(None),
    user_creator_issue_fk: int = Query(None),
    user_informator_fk: int = Query(None),
    sprint_id_fk: int = Query(None),
    status_issue: int = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    try:
        pool: Pool = get_pool()  # obtiene el pool desde connection.py
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return await get_issues_controller(
        db_pool=pool,
        issue_id=issue_id,
        summary=summary,
        description=description,
        audit_id=audit_id,
        resolve_at=resolve_at,
        due_date=due_date,
        votes=votes,
        original_estimation=original_estimation,
        custom_start_date=custom_start_date,
        story_point_estimate=story_point_estimate,
        parent_summary=parent_summary,
        issue_type=issue_type,
        project_id_fk=project_id_fk,
        user_assigned_fk=user_assigned_fk,
        user_creator_issue_fk=user_creator_issue_fk,
        user_informator_fk=user_informator_fk,
        sprint_id_fk=sprint_id_fk,
        status_issue=status_issue,
        page=page,
        limit=limit
    )

@router.delete("/{issue_id}")
async def delete_issue(issue_id: int):
    try:
        pool: Pool = get_pool()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return await delete_issue_controller(db_pool=pool, issue_id=issue_id)
