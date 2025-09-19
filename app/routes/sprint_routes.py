from datetime import date
from fastapi import APIRouter, Depends,Query
from typing import List, Optional
from asyncpg import Pool
from app.schemas.sprint import SprintResponse, SprintCreate
from app.controllers.sprint_controller import (
    get_sprint_controller,
    post_sprint_controller,
    patch_sprint_controller,
    put_sprint_controller,
    delete_sprint_controller
)
from app.database.conection import get_pool
router = APIRouter(prefix="/sprint", tags=["Sprint"])



@router.get("/", response_model=SprintResponse)
async def list_sprints(
    sprint_id: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    date_init_start: Optional[str] = None,
    date_init_end: Optional[str] = None,
    date_end_start: Optional[str] = None,
    date_end_end: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db_pool: Pool = Depends(get_pool)
):
    return await get_sprint_controller(
        db_pool, sprint_id, name, description,
        date_init_start, date_init_end,
        date_end_start, date_end_end,
        page, limit
    )

@router.post("/", response_model=List[dict])
async def create_sprint(sprint: SprintCreate, db_pool: Pool = Depends(get_pool)):
    return await post_sprint_controller(db_pool, sprint.dict())

@router.patch("/")
async def patch_sprint(
    sprint_id: int = Query(...),
    name: str = Query(None),
    description: str = Query(None),
    date_init: date = Query(None),
    date_end: date = Query(None),
    db_pool: Pool = Depends(get_pool)
):
    return await patch_sprint_controller(db_pool, sprint_id, name, description, date_init, date_end)

@router.put("/")
async def put_sprint(
    sprint_id: int = Query(...),
    name: str = Query(...),
    description: str = Query(...),
    date_init: date = Query(...),
    date_end: date = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await put_sprint_controller(db_pool, sprint_id, name, description, date_init, date_end)

@router.delete("/{sprint_id}")
async def delete_sprint(sprint_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_sprint_controller(db_pool, sprint_id)