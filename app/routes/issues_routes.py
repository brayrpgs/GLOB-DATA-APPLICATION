from fastapi import APIRouter, Query, HTTPException, Depends, Path
from fastapi.responses import JSONResponse
import logging
from asyncpg import Pool
from app.controllers.issue_controller import (
    post_issue_controller,
    get_issue_controller,
    patch_issue_controller,
    put_issue_controller,
    delete_issue_controller
)
from app.database.conection import get_pool
from app.schemas.issue import IssueCreate, IssuePatchRequest, IssuePutRequest

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/issues",
    tags=["issues"]
)

@router.post("/", responses={
    201: {
        "description": "Created",
        "content": {
            "application/json": {
                "example": {"success": True, "data": {"issue_id": 1, "summary": "Example issue"}}
            }
        }
    },
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "Required fields are missing"}}}
    },
    500: {
        "description": "Internal Server Error siiiii",
        "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}
    }
})
async def create_issue(
    issue: IssueCreate,
    db_pool: Pool = Depends(get_pool)
):
    """Create an issue by accepting a JSON body matching IssueCreate schema."""
    try:
        result = await post_issue_controller(db_pool, issue)
        
        status_code = None
        if isinstance(result, dict):
            if isinstance(result.get("status_code"), int):
                status_code = result.pop("status_code")
            elif isinstance(result.get("code"), int):
                status_code = result.pop("code")
            elif result.get("success") is False or str(result.get("status")).lower() in ("error", "fail"):
                status_code = 400

        if status_code is None:
            status_code = 201

        return JSONResponse(status_code=status_code, content=result)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in create_issue: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error siiiiiii"})

@router.get("/")
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
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool)
):
    return await get_issue_controller(
        db_pool, issue_id, summary, description, audit_id, resolve_at,
        due_date, votes, original_estimation, custom_start_date,
        story_point_estimate, parent_summary, issue_type, project_id_fk,
        user_assigned_fk, user_creator_issue_fk, user_informator_fk,
        sprint_id_fk, status_issue, page, limit
    )

@router.patch("/{issue_id}", responses={
    200: {
        "description": "Patched",
        "content": {"application/json": {"example": {"success": True, "data": {"issue_id": 1}}}}
    },
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "Provide at least one field to update"}}}
    },
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Issue not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}}
})
async def patch_issue(
    issue: IssuePatchRequest,
    issue_id: int = Path(..., description="ID of the issue to patch"),
    db_pool: Pool = Depends(get_pool)
):
    """Partially update an issue identified by `issue_id`."""
    update_data = issue.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Provide at least one field to update")

    try:
        result = await patch_issue_controller(db_pool, issue_id, issue)
        
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Issue not found"})

        status_code = None
        if isinstance(result, dict):
            if isinstance(result.get("status_code"), int):
                status_code = result.pop("status_code")
            elif isinstance(result.get("code"), int):
                status_code = result.pop("code")
            elif result.get("success") is False or str(result.get("status")).lower() in ("error", "fail"):
                status_code = 400

        if status_code is None:
            status_code = 200

        return JSONResponse(status_code=status_code, content=result)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in patch_issue: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@router.put("/{issue_id}", responses={
    200: {
        "description": "Updated",
        "content": {"application/json": {"example": {"success": True, "data": {"issue_id": 1}}}}
    },
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "Required fields are missing"}}}
    },
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Issue not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}}
})
async def put_issue(
    issue: IssuePutRequest,
    issue_id: int = Path(..., description="ID of the issue to update"),
    db_pool: Pool = Depends(get_pool)
):
    """Fully replace an issue identified by path parameter `issue_id`."""
    try:
        result = await put_issue_controller(db_pool, issue_id, issue)
        
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Issue not found"})
        
        status_code = None
        if isinstance(result, dict):
            if isinstance(result.get("status_code"), int):
                status_code = result.pop("status_code")
            elif isinstance(result.get("code"), int):
                status_code = result.pop("code")
            elif result.get("success") is False or str(result.get("status")).lower() in ("error", "fail"):
                status_code = 400

        if status_code is None:
            status_code = 200

        return JSONResponse(status_code=status_code, content=result)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in put_issue: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@router.delete("/{issue_id}", responses={
    200: {"description": "Deleted", "content": {"application/json": {"example": {"success": True}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Issue not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}}
})
async def delete_issue(
    issue_id: int = Path(..., description="ID of the issue to delete"),
    db_pool: Pool = Depends(get_pool)
):
    try:
        result = await delete_issue_controller(db_pool, issue_id)
        
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Issue not found"})

        status_code = None
        if isinstance(result, dict):
            if isinstance(result.get("status_code"), int):
                status_code = result.pop("status_code")
            elif isinstance(result.get("code"), int):
                status_code = result.pop("code")
            elif result.get("success") is False or str(result.get("status")).lower() in ("error", "fail"):
                status_code = 400

        if status_code is None:
            status_code = 200

        return JSONResponse(status_code=status_code, content=result)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in delete_issue: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
