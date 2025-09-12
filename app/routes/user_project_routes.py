from fastapi import APIRouter, Query, HTTPException, status, Body
from typing import List, Optional
from decimal import Decimal

from app.database.conection import get_connection
from app.schemas.user_project import UserProjectSchema, UserProjectCreateSchema

router = APIRouter(prefix="/user-projects", tags=["User Projects"])


@router.post("/", response_model=UserProjectSchema, status_code=status.HTTP_201_CREATED)
def create_user_project(user_project: UserProjectCreateSchema):
    """
    Create a new user project using POST_USER_PROJECT stored procedure.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "POST_USER_PROJECT",
                [user_project.user_id_fk, user_project.rol_proyect, user_project.productivity],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=500, detail="UserProject could not be created")

            created = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return created


@router.get("/", response_model=List[UserProjectSchema])
def get_user_projects(
    user_project_id: Optional[int] = Query(None),
    user_id_fk: Optional[int] = Query(None),
    rol_proyect: Optional[int] = Query(None),
    productivity: Optional[Decimal] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    """
    Get a list of user projects using GET_USER_PROJECT stored procedure.
    Supports filtering and pagination.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "GET_USER_PROJECT",
                [user_project_id, user_id_fk, rol_proyect, productivity, page, limit],
            )
            result = cur.fetchone()
            data = result["data"] if result and "data" in result else []

    return data


@router.patch("/{user_project_id}", response_model=UserProjectSchema)
def patch_user_project(user_project_id: int, user_project: UserProjectCreateSchema = Body(...)):
    """
    Partially update a user project using PATCH_USER_PROJECT stored procedure.
    Only provided fields will be updated.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PATCH_USER_PROJECT",
                [user_project_id, user_project.user_id_fk, user_project.rol_proyect, user_project.productivity],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"UserProject with ID {user_project_id} not found")

            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return updated


@router.put("/{user_project_id}", response_model=UserProjectSchema)
def put_user_project(user_project_id: int, user_project: UserProjectCreateSchema):
    """
    Fully update a user project using PUT_USER_PROJECT stored procedure.
    All fields must be provided.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PUT_USER_PROJECT",
                [user_project_id, user_project.user_id_fk, user_project.rol_proyect, user_project.productivity],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"UserProject with ID {user_project_id} not found")

            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return updated


@router.delete("/{user_project_id}", response_model=UserProjectSchema)
def delete_user_project(user_project_id: int):
    """
    Delete a user project using DELETE_USER_PROJECT stored procedure.
    Returns the deleted user project.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("DELETE_USER_PROJECT", [user_project_id])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"UserProject with ID {user_project_id} not found")

            deleted = result["data"]

    return deleted
