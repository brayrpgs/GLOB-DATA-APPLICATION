from fastapi import APIRouter, Query, HTTPException, status, Body
from typing import List, Optional
from datetime import date

from app.database.conection import get_connection
from app.schemas.sprint import SprintSchema, SprintCreateSchema

router = APIRouter(prefix="/sprints", tags=["Sprints"])


@router.post("/", response_model=SprintSchema, status_code=status.HTTP_201_CREATED)
def create_sprint(sprint: SprintCreateSchema):
    """
    Create a new sprint using POST_SPRINT stored procedure.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "POST_SPRINT",
                [sprint.name, sprint.description, sprint.date_init, sprint.date_end],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=500, detail="Sprint could not be created")

            created = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return created


@router.get("/", response_model=List[SprintSchema])
def get_sprints(
    sprint_id: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    date_init_start: Optional[date] = Query(None),
    date_init_end: Optional[date] = Query(None),
    date_end_start: Optional[date] = Query(None),
    date_end_end: Optional[date] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    """
    Get a list of sprints using GET_SPRINT stored procedure.
    Supports filtering and pagination.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "GET_SPRINT",
                [
                    sprint_id,
                    name,
                    description,
                    date_init_start,
                    date_init_end,
                    date_end_start,
                    date_end_end,
                    page,
                    limit,
                ],
            )
            result = cur.fetchone()
            data = result["data"] if result and "data" in result else []

    return data


@router.patch("/{sprint_id}", response_model=SprintSchema)
def patch_sprint(sprint_id: int, sprint: SprintCreateSchema = Body(...)):
    """
    Partially update a sprint using PATCH_SPRINT stored procedure.
    Only provided fields will be updated.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PATCH_SPRINT",
                [sprint_id, sprint.name, sprint.description, sprint.date_init, sprint.date_end],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"Sprint with ID {sprint_id} not found")

            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return updated


@router.put("/{sprint_id}", response_model=SprintSchema)
def put_sprint(sprint_id: int, sprint: SprintCreateSchema):
    """
    Fully update a sprint using PUT_SPRINT stored procedure.
    All fields must be provided.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PUT_SPRINT",
                [sprint_id, sprint.name, sprint.description, sprint.date_init, sprint.date_end],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"Sprint with ID {sprint_id} not found")

            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return updated


@router.delete("/{sprint_id}", response_model=SprintSchema)
def delete_sprint(sprint_id: int):
    """
    Delete a sprint using DELETE_SPRINT stored procedure.
    Returns the deleted sprint.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("DELETE_SPRINT", [sprint_id])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"Sprint with ID {sprint_id} not found")

            deleted = result["data"]

    return deleted
