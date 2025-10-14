from fastapi import APIRouter, Depends, Query, HTTPException, Path
from asyncpg import Pool
from app.controllers.user_project_controller import (
    post_user_project_controller,
    get_user_project_controller,
    patch_user_project_controller,
    put_user_project_controller,
    delete_user_project_controller,
)
from app.database.conection import get_pool
from decimal import Decimal
from typing import Optional
from fastapi.responses import JSONResponse
import logging

from app.schemas.user_project import (
    UserProjectCreate,
    UserProjectPatch,
    UserProjectPut,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user-projects", tags=["user-projects"])


@router.post("/", responses={
    201: {"description": "Created", "content": {"application/json": {"example": {"success": True, "data": {"id": 1}}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "required fields missing"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def create_user_project(user_project: UserProjectCreate, db_pool: Pool = Depends(get_pool)):
    if user_project.rol_proyect is None or user_project.productivity is None:
        raise HTTPException(status_code=400, detail="rol_proyect and productivity are required")

    try:
        result = await post_user_project_controller(db_pool, user_project.user_id_fk, user_project.rol_proyect, user_project.productivity)

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
        logger.exception("Unexpected error in create_user_project: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@router.get("/")
async def get_user_projects(
    user_project_id: Optional[int] = Query(None),
    user_id_fk: Optional[int] = Query(None),
    rol_proyect: Optional[int] = Query(None),
    productivity: Optional[Decimal] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool),
):
    try:
        return await get_user_project_controller(db_pool, user_project_id, user_id_fk, rol_proyect, productivity, page, limit)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error in get_user_projects: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{user_project_id}", responses={
    200: {"description": "Patched", "content": {"application/json": {"example": {"success": True}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "Provide at least one field to update"}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "User project not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def patch_user_project(
    user_project: UserProjectPatch,
    user_project_id: int = Path(..., description="ID of the user_project to patch"),
    db_pool: Pool = Depends(get_pool),
):
    provided_user_fk = user_project.user_id_fk is not None
    provided_role = user_project.rol_proyect is not None
    provided_productivity = user_project.productivity is not None
    if not (provided_user_fk or provided_role or provided_productivity):
        raise HTTPException(status_code=400, detail="Provide at least one field to update")

    try:
        result = await patch_user_project_controller(db_pool, user_project_id, user_project.user_id_fk, user_project.rol_proyect, user_project.productivity)
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "User project not found"})

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
        logger.exception("Unexpected error in patch_user_project: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@router.put("/{user_project_id}", responses={
    200: {"description": "Updated", "content": {"application/json": {"example": {"success": True}}}},
    400: {"description": "Bad Request", "content": {"application/json": {"example": {"detail": "All fields are required"}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "User project not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def put_user_project(
    user_project: UserProjectPut,
    user_project_id: int = Path(..., description="ID of the user_project to update"),
    db_pool: Pool = Depends(get_pool),
):
    if user_project.rol_proyect is None or user_project.productivity is None:
        raise HTTPException(status_code=400, detail="rol_proyect and productivity are required")

    try:
        result = await put_user_project_controller(db_pool, user_project_id, user_project.user_id_fk, user_project.rol_proyect, user_project.productivity)
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "User project not found"})

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
        logger.exception("Unexpected error in put_user_project: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@router.delete("/{user_project_id}", responses={
    200: {"description": "Deleted", "content": {"application/json": {"example": {"success": True}}}},
    404: {"description": "Not Found", "content": {"application/json": {"example": {"detail": "User project not found"}}}},
    500: {"description": "Internal Server Error", "content": {"application/json": {"example": {"detail": "Internal Server Error"}}}},
})
async def delete_user_project(user_project_id: int = Path(..., description="ID of the user_project to delete"), db_pool: Pool = Depends(get_pool)):
    try:
        result = await delete_user_project_controller(db_pool, user_project_id)
        if result is None:
            return JSONResponse(status_code=404, content={"detail": "User project not found"})

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
        logger.exception("Unexpected error in delete_user_project: %s", e)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})