from fastapi import APIRouter, Query, Depends, HTTPException, Path
from fastapi.responses import JSONResponse
import logging
from asyncpg import Pool
from app.controllers.issue_type_controller import (
    post_issue_type_controller,
    get_issue_type_controller,
    patch_issue_type_controller,
    put_issue_type_controller,
    delete_issue_type_controller
)
from app.database.conection import get_pool
from app.schemas.issue_type import IssueTypeCreate

router = APIRouter(
    prefix="/issue-types",
    tags=["issue-types"]
)

@router.post("/", responses={
    201: {
        "description": "Created",
        "content": {
            "application/json": {
                "example": {"success": True, "data": {"id": 1, "status": 1, "priority": 2}}
            }
        }
    },
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "status and priority are required fields"}}}
    },
    500: {
        "description": "Internal Server Error",
        "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}
    }
})
async def create_issue_type(
    issue_type: IssueTypeCreate,
    db_pool: Pool = Depends(get_pool)
):
    """Create an issue type by accepting a JSON body matching IssueTypeCreate schema."""
    # Validate required fields
    if issue_type.status is None or issue_type.priority is None:
        raise HTTPException(status_code=400, detail="status and priority are required fields")
    # Extract fields from the body and forward to the controller
    try:
        result = await post_issue_type_controller(db_pool, issue_type.status, issue_type.priority)
        # Controller should raise HTTPException on errors; otherwise map result to status codes below

        # Determine status code from result if present
        status_code = None
        if isinstance(result, dict):
            if isinstance(result.get("status_code"), int):
                status_code = result.pop("status_code")
            elif isinstance(result.get("code"), int):
                status_code = result.pop("code")
            elif result.get("success") is False or str(result.get("status")).lower() in ("error", "fail"):
                status_code = 400

        # Default to 201 Created for successful POST
        if status_code is None:
            status_code = 201

        return JSONResponse(status_code=status_code, content=result)
    except HTTPException:
        # re-raise so FastAPI returns the provided status and detail
        raise
    except Exception as e:
        logging.exception("Unexpected error in create_issue_type: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@router.get("/")
async def get_issue_types(
    issue_type_id: int = Query(None),
    status: int = Query(None),
    priority: int = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool)
):
    return await get_issue_type_controller(db_pool, issue_type_id, status, priority, page, limit)

@router.patch("/{issue_type_id}", responses={
    200: {
        "description": "Patched",
        "content": {"application/json": {"example": {"success": True, "data": {"id": 1, "status": 1, "priority": 2}}}}
    },
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "Provide exactly one of status or priority"}}}
    },
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Issue type not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}}
})
async def patch_issue_type(
    issue_type: IssueTypeCreate,
    issue_type_id: int = Path(..., description="ID of the issue type to patch"),
    db_pool: Pool = Depends(get_pool)
):
    """Partially update an issue type identified by `issue_type_id`.

    Provide at least one of `status` or `priority` in the JSON body.
    """
    # Require exactly one field to patch (either status xor priority)
    provided_status = issue_type.status is not None
    provided_priority = issue_type.priority is not None
    if not (provided_status ^ provided_priority):
        # XOR: True only when exactly one is provided
        raise HTTPException(status_code=400, detail="Provide exactly one of status or priority")

    try:
        result = await patch_issue_type_controller(db_pool, issue_type_id, issue_type.status, issue_type.priority)
        # If controller returns None (not found), respond 404
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Issue type not found"})

        # Map controller result to proper status code if provided
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
        logging.exception("Unexpected error in patch_issue_type: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@router.put("/{issue_type_id}", responses={
    200: {
        "description": "Updated",
        "content": {"application/json": {"example": {"success": True, "data": {"id": 1, "status": 1, "priority": 2}}}}
    },
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "status and priority are required fields"}}}
    },
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Issue type not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}}
})
async def put_issue_type(
    issue_type: IssueTypeCreate,
    issue_type_id: int = Path(..., description="ID of the issue type to update"),
    db_pool: Pool = Depends(get_pool)
):
    """Fully replace an issue type identified by path parameter `issue_type_id` using a JSON body.

    The body must include `status` and `priority` fields. Returns the updated resource on success.
    """
    # Validate required fields in body
    if issue_type.status is None or issue_type.priority is None:
        raise HTTPException(status_code=400, detail="status and priority are required fields")

    try:
        result = await put_issue_type_controller(db_pool, issue_type_id, issue_type.status, issue_type.priority)
        # If controller returns None (not found), respond 404
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Issue type not found"})
        # Map controller result to proper status code if provided
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
        logging.exception("Unexpected error in put_issue_type: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@router.delete("/{issue_type_id}")
async def delete_issue_type(issue_type_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_issue_type_controller(db_pool, issue_type_id)
