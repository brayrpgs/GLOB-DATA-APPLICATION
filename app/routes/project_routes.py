
from fastapi import APIRouter, Depends, Query, HTTPException, Path
from fastapi.responses import JSONResponse
from typing import Optional
from asyncpg import Pool
import logging

from app.database.conection import get_pool
from app.schemas.project import (
    ProjectResponse,
    ProjectCreate,
    ProjectPatch,
    ProjectPut,
)
from app.controllers.project_controller import (
    post_project_controller,
    get_project_controller,
    patch_project_controller,
    put_project_controller,
    delete_project_controller,
)

logger = logging.getLogger(__name__)

# Use plural and consistent tag as other routes
router = APIRouter(prefix="/projects", tags=["projects"]) 


@router.post("/", responses={
    201: {"description": "Created", "content": {"application/json": {"example": {"success": True, "data": {"id": 1}}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "required fields missing"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def create_project(project: ProjectCreate, db_pool: Pool = Depends(get_pool)):
    # Validate required fields manually so we can return 400 instead of FastAPI's 422
    if (
        project.name is None
        or project.description is None
        or project.date_init is None
        or project.date_end is None
        or project.status is None
        or project.progress is None
    ):
        raise HTTPException(status_code=400, detail="name, description, date_init, date_end, status and progress are required")

    try:
        result = await post_project_controller(
            db_pool,
            project.name,
            project.description,
            project.user_project_id_fk,
            project.date_init,
            project.date_end,
            project.status,
            project.progress,
        )

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
        logger.exception("Unexpected error in create_project: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@router.get("/", response_model=ProjectResponse)
async def get_projects(
    project_id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    user_project_id_fk: Optional[int] = Query(None),
    date_init_start: Optional[str] = Query(None),
    date_init_end: Optional[str] = Query(None),
    date_end_start: Optional[str] = Query(None),
    date_end_end: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    progress_min: Optional[float] = Query(None),
    progress_max: Optional[float] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool),
):
    filters = {
        "project_id": project_id,
        "name": name,
        "description": description,
        "user_project_id_fk": user_project_id_fk,
        "date_init_start": date_init_start,
        "date_init_end": date_init_end,
        "date_end_start": date_end_start,
        "date_end_end": date_end_end,
        "status": status,
        "progress_min": progress_min,
        "progress_max": progress_max,
    }
    try:
        return await get_project_controller(db_pool, filters, page, limit)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in get_projects: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{project_id}", responses={
    200: {"description": "Patched", "content": {"application/json": {"example": {"success": True}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "Provide at least one field to update"}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Project not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def patch_project(
    project: ProjectPatch,
    project_id: int = Path(..., description="ID of the project to patch"),
    db_pool: Pool = Depends(get_pool),
):
    # Require at least one field to patch
    provided_name = project.name is not None
    provided_description = project.description is not None
    provided_user_fk = project.user_project_id_fk is not None
    provided_date_init = project.date_init is not None
    provided_date_end = project.date_end is not None
    provided_status = project.status is not None
    provided_progress = project.progress is not None
    if not (
        provided_name
        or provided_description
        or provided_user_fk
        or provided_date_init
        or provided_date_end
        or provided_status
        or provided_progress
    ):
        raise HTTPException(status_code=400, detail="Provide at least one field to update")

    try:
        result = await patch_project_controller(
            db_pool,
            project_id,
            project.name,
            project.description,
            project.user_project_id_fk,
            project.date_init,
            project.date_end,
            project.status,
            project.progress,
        )
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Project not found"})

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
        logger.exception("Unexpected error in patch_project: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@router.put("/{project_id}", responses={
    200: {"description": "Updated", "content": {"application/json": {"example": {"success": True}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "All fields are required"}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Project not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def put_project(
    project: ProjectPut,
    project_id: int = Path(..., description="ID of the project to update"),
    db_pool: Pool = Depends(get_pool),
):
    # Validate required fields manually so we can return 400 instead of FastAPI's 422
    if (
        project.name is None
        or project.description is None
        or project.date_init is None
        or project.date_end is None
        or project.status is None
        or project.progress is None
    ):
        raise HTTPException(status_code=400, detail="name, description, date_init, date_end, status and progress are required")

    try:
        result = await put_project_controller(
            db_pool,
            project_id,
            project.name,
            project.description,
            project.user_project_id_fk,
            project.date_init,
            project.date_end,
            project.status,
            project.progress,
        )
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Project not found"})

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
        logger.exception("Unexpected error in put_project: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@router.delete("/{project_id}", responses={
    200: {"description": "Deleted", "content": {"application/json": {"example": {"success": True}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "Project not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def delete_project(project_id: int = Path(..., description="ID of the project to delete"), db_pool: Pool = Depends(get_pool)):
    try:
        result = await delete_project_controller(db_pool, project_id)
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "Project not found"})

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
        logger.exception("Unexpected error in delete_project: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
