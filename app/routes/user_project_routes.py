from fastapi import APIRouter, Query, Depends
from asyncpg import Pool
from app.controllers.user_project_controller import (
    post_user_project_controller,
    get_user_project_controller,
    patch_user_project_controller,
    put_user_project_controller,
    delete_user_project_controller
)
from app.database.conection import get_pool
from decimal import Decimal
from typing import Optional

router = APIRouter(
    prefix="/user-projects",
    tags=["user-projects"]
)

@router.post("/")
async def create_user_project(
    user_id_fk: int = Query(...),
    rol_proyect: int = Query(...),
    productivity: Decimal = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await post_user_project_controller(db_pool, user_id_fk, rol_proyect, productivity)

@router.get("/")
async def get_user_projects(
    user_project_id: Optional[int] = Query(None),
    user_id_fk: Optional[int] = Query(None),
    rol_proyect: Optional[int] = Query(None),
    productivity: Optional[Decimal] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool)
):
    return await get_user_project_controller(db_pool, user_project_id, user_id_fk, rol_proyect, productivity, page, limit)

@router.patch("/")
async def patch_user_project(
    user_project_id: int = Query(...),
    user_id_fk: Optional[int] = Query(None),
    rol_proyect: Optional[int] = Query(None),
    productivity: Optional[Decimal] = Query(None),
    db_pool: Pool = Depends(get_pool)
):
    return await patch_user_project_controller(db_pool, user_project_id, user_id_fk, rol_proyect, productivity)

@router.put("/")
async def put_user_project(
    user_project_id: int = Query(...),
    user_id_fk: int = Query(...),
    rol_proyect: int = Query(...),
    productivity: Decimal = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await put_user_project_controller(db_pool, user_project_id, user_id_fk, rol_proyect, productivity)

@router.delete("/{user_project_id}")
async def delete_user_project(user_project_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_user_project_controller(db_pool, user_project_id)