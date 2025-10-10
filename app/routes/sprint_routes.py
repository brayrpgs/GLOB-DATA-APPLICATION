from datetime import date
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from fastapi.responses import JSONResponse
from typing import List, Optional
from asyncpg import Pool
import logging

from app.schemas.sprint import SprintResponse, SprintCreate, SprintPatchRequest, SprintPutRequest
from app.controllers.sprint_controller import (
    get_sprint_controller,
    post_sprint_controller,
    patch_sprint_controller,
    put_sprint_controller,
    delete_sprint_controller,
)
from app.database.conection import get_pool

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sprints", tags=["sprints"])


@router.get("/", response_model=SprintResponse)
async def list_sprints(
    sprint_id: int = Query(None),
    name: str = Query(None),
    description: str = Query(None),
    date_init_start: str = Query(None),
    date_init_end: str = Query(None),
    date_end_start: str = Query(None),
    date_end_end: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool),
):
    # Delegate to controller which handles DB errors and returns the proper dict
    return await get_sprint_controller(
        db_pool,
        sprint_id,
        name,
        description,
        date_init_start,
        date_init_end,
        date_end_start,
        date_end_end,
        page,
        limit,
    )


@router.post("/", responses={
    201: {"description": "Created", "content": {"application/json": {"example": {"success": True, "data": {"id": 1}}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "name, description, date_init and date_end are required"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def create_sprint(sprint: SprintCreate, db_pool: Pool = Depends(get_pool)):
    # Validate required fields manually so we can return 400 instead of FastAPI's 422
    if sprint.name is None or sprint.description is None or sprint.date_init is None or sprint.date_end is None:
        raise HTTPException(status_code=400, detail="name, description, date_init and date_end are required")

    try:
        result = await post_sprint_controller(db_pool, sprint.dict())

        # Determine status code from result if present
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
        logger.exception("Unexpected error in create_sprint: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@router.patch("/{sprint_id}", responses={
    200: {"description": "Patched", "content": {"application/json": {"example": {"success": True}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "Provide at least one field to update"}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Sprint not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def patch_sprint(
    sprint: SprintPatchRequest,
    sprint_id: int = Path(..., description="ID of the sprint to patch"),
    db_pool: Pool = Depends(get_pool),
):
    # Require at least one field to patch
    provided_name = sprint.name is not None
    provided_description = sprint.description is not None
    provided_date_init = sprint.date_init is not None
    provided_date_end = sprint.date_end is not None
    if not (provided_name or provided_description or provided_date_init or provided_date_end):
        raise HTTPException(status_code=400, detail="Provide at least one field to update")

    try:
        result = await patch_sprint_controller(
            db_pool, sprint_id, sprint.name, sprint.description, sprint.date_init, sprint.date_end
        )
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Sprint not found"})

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
        logger.exception("Unexpected error in patch_sprint: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@router.put("/{sprint_id}", responses={
    200: {"description": "Updated", "content": {"application/json": {"example": {"success": True}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "All fields are required"}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Sprint not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def put_sprint(
    sprint: SprintPutRequest,
    sprint_id: int = Path(..., description="ID of the sprint to update"),
    db_pool: Pool = Depends(get_pool),
):
    # Validate required fields manually so we can return 400 instead of FastAPI's 422
    if sprint.name is None or sprint.description is None or sprint.date_init is None or sprint.date_end is None:
        raise HTTPException(status_code=400, detail="name, description, date_init and date_end are required")

    try:
        result = await put_sprint_controller(
            db_pool, sprint_id, sprint.name, sprint.description, sprint.date_init, sprint.date_end
        )
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Sprint not found"})

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
        logger.exception("Unexpected error in put_sprint: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@router.delete("/{sprint_id}", responses={
    200: {"description": "Deleted", "content": {"application/json": {"example": {"success": True}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Sprint not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def delete_sprint(sprint_id: int = Path(..., description="ID of the sprint to delete"), db_pool: Pool = Depends(get_pool)):
    try:
        result = await delete_sprint_controller(db_pool, sprint_id)
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Sprint not found"})

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
        logger.exception("Unexpected error in delete_sprint: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})