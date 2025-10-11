from datetime import date
from typing import Optional
from fastapi import APIRouter, Query, HTTPException, Depends, Path
from asyncpg import Pool
from app.controllers.issue_controller import get_issues_controller,delete_issue_controller,post_issue_controller,patch_issue_controller,put_issue_controller
from app.schemas.issue import IssueResponse, IssuePatchRequest, IssuePutRequest, IssueCreate
from app.database.conection import get_pool

router = APIRouter(
    prefix="/issues",
    tags=["issues"]
)
@router.post("/", status_code=201, responses={
    201: {"description": "Issue created successfully"},
    422: {"description": "Validation Error"},
    500: {"description": "Internal Server Error"}
})
async def create_issue(issue: IssueCreate, db_pool: Pool = Depends(get_pool)):
    """
    Creates a new issue.
    """
    # The Pydantic model `IssueCreate` handles validation for required fields.
    # FastAPI will return a 422 if the request body is invalid.
    try:
        return await post_issue_controller(db_pool, issue.dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

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
, db_pool: Pool = Depends(get_pool)):
    return await get_issues_controller(
        db_pool=db_pool,
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
    
@router.patch("/{issue_id}", responses={
    200: {"description": "Issue updated successfully"},
    404: {"description": "Issue not found"},
    500: {"description": "Internal Server Error"}
})
async def patch_issue(issue_update: IssuePatchRequest, issue_id: int = Path(..., description="The ID of the issue to patch"), db_pool: Pool = Depends(get_pool)):
    """
    Partially updates an issue using PATCH_ISSUE SP.
    """
    # Set the issue_id from the path into the request object
    issue_update.issue_id = issue_id
    return await patch_issue_controller(db_pool, issue_update)

@router.put("/{issue_id}", responses={
    200: {"description": "Issue replaced successfully"},
    404: {"description": "Issue not found"},
    422: {"description": "Validation Error"},
    500: {"description": "Internal Server Error"}
})
async def put_issue(issue_replace: IssuePutRequest, issue_id: int = Path(..., description="The ID of the issue to replace"), db_pool: Pool = Depends(get_pool)):
    """
    Completely replaces an issue using PUT_ISSUE SP.
    """
    # Set the issue_id from the path into the request object
    issue_replace.issue_id = issue_id
    return await put_issue_controller(db_pool, issue_replace)

@router.delete("/{issue_id}", responses={
    200: {"description": "Issue deleted successfully"},
    404: {"description": "Issue not found"},
    500: {"description": "Internal Server Error"}
})
async def delete_issue(issue_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_issue_controller(db_pool=db_pool, issue_id=issue_id)
