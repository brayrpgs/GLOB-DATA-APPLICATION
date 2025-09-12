from fastapi import APIRouter, Query, HTTPException, status, Body
from typing import List, Optional
from datetime import date
from decimal import Decimal

from app.database.conection import get_connection
from app.schemas.project import ProjectSchema, ProjectCreateSchema

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreateSchema):
    """
    Create a new project using the stored procedure POST_PROJECT.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "POST_PROJECT",
                [
                    project.name,
                    project.description,
                    project.user_project_id_fk,
                    project.date_init,
                    project.date_end,
                    project.status,
                    project.progress,
                ],
            )
            result = cur.fetchone()

            if not result or not result.get("data"):
                raise HTTPException(
                    status_code=500,
                    detail="Project could not be created"
                )

            created = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return created


@router.get("/", response_model=List[ProjectSchema])
def get_projects(
    project_id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    user_project_id_fk: Optional[int] = Query(None),
    date_init_start: Optional[date] = Query(None),
    date_init_end: Optional[date] = Query(None),
    date_end_start: Optional[date] = Query(None),
    date_end_end: Optional[date] = Query(None),
    status_param: Optional[int] = Query(None, alias="status"),
    progress_min: Optional[Decimal] = Query(None),
    progress_max: Optional[Decimal] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    """
    Get a list of projects using the stored procedure GET_PROJECT.
    Supports filtering and pagination.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "GET_PROJECT",
                [
                    project_id,
                    name,
                    description,
                    user_project_id_fk,
                    date_init_start,
                    date_init_end,
                    date_end_start,
                    date_end_end,
                    status_param,
                    progress_min,
                    progress_max,
                    page,
                    limit,
                ],
            )
            result = cur.fetchone()
            data = result["data"] if result and "data" in result else []

    return data


@router.patch("/{project_id}", response_model=ProjectSchema)
def patch_project(project_id: int, project: ProjectCreateSchema = Body(...)):
    """
    Partially update a project using PATCH_PROJECT.
    Only provided fields will be updated.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PATCH_PROJECT",
                [
                    project_id,
                    project.name,
                    project.description,
                    project.user_project_id_fk,
                    project.date_init,
                    project.date_end,
                    project.status,
                    project.progress,
                ],
            )
            result = cur.fetchone()

            if not result or not result.get("data"):
                raise HTTPException(
                    status_code=404,
                    detail=f"Project with ID {project_id} not found"
                )

            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return updated


@router.put("/{project_id}", response_model=ProjectSchema)
def put_project(project_id: int, project: ProjectCreateSchema):
    """
    Fully update a project using PUT_PROJECT.
    All fields must be provided.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PUT_PROJECT",
                [
                    project_id,
                    project.name,
                    project.description,
                    project.user_project_id_fk,
                    project.date_init,
                    project.date_end,
                    project.status,
                    project.progress,
                ],
            )
            result = cur.fetchone()

            if not result or not result.get("data"):
                raise HTTPException(
                    status_code=404,
                    detail=f"Project with ID {project_id} not found"
                )

            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return updated


@router.delete("/{project_id}", response_model=ProjectSchema)
def delete_project(project_id: int):
    """
    Delete a project using DELETE_PROJECT.
    Returns the deleted project.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("DELETE_PROJECT", [project_id])
            result = cur.fetchone()

            if not result or not result.get("data"):
                raise HTTPException(
                    status_code=404,
                    detail=f"Project with ID {project_id} not found"
                )

            deleted = result["data"]

    return deleted
