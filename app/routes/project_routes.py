from datetime import date
from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from typing import Optional
from asyncpg import Pool
from app.database.conection import get_pool
from app.schemas.project import (
    ProjectResponse
)
from app.controllers.project_controller import (
    post_project_controller,
    get_project_controller,
    patch_project_controller,
    put_project_controller,
    delete_project_controller,
)

router = APIRouter(prefix="/project", tags=["Project"])

@router.post("/")
async def create_project(
    name: str = Query(...),
    description: str = Query(...),
    user_project_id_fk: int = Query(...),
    date_init: date = Query(...),
    date_end: date = Query(...),
    status: int = Query(...),
    progress: Decimal = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await post_project_controller(db_pool, name, description, user_project_id_fk, date_init, date_end, status, progress)

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
    page: int = Query(1),
    limit: int = Query(10),
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
    return await get_project_controller(db_pool, filters, page, limit)

@router.patch("/")
async def patch_project(
    project_id: int = Query(...),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    user_project_id_fk: Optional[int] = Query(None),
    date_init: Optional[date] = Query(None),
    date_end: Optional[date] = Query(None),
    status: Optional[int] = Query(None),
    progress: Optional[Decimal] = Query(None),
    db_pool: Pool = Depends(get_pool)
):
    return await patch_project_controller(db_pool, project_id, name, description, user_project_id_fk, date_init, date_end, status, progress)

@router.put("/")
async def put_project(
    project_id: int = Query(...),
    name: str = Query(...),
    description: str = Query(...),
    user_project_id_fk: int = Query(...),
    date_init: date = Query(...),
    date_end: date = Query(...),
    status: int = Query(...),
    progress: Decimal = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await put_project_controller(db_pool, project_id, name, description, user_project_id_fk, date_init, date_end, status, progress)

@router.delete("/{project_id}", response_model=dict)
async def delete_project(project_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_project_controller(db_pool, project_id)
