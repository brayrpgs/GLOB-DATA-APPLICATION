from fastapi import APIRouter, HTTPException, status, Body, Query
from typing import List, Optional

from app.database.conection import get_connection
from app.schemas.user import UserSchema, UserCreateSchema

router = APIRouter(prefix="/account", tags=["Account"])


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_account(data: UserCreateSchema):
    """
    Create a new user account.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "POST_ACCOUNT",
                [
                    data.email,
                    data.username,
                    data.hashed_password,
                    data.avatar_url,
                    data.status
                ],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=500, detail="User could not be created")
            created = result["data"][0] if isinstance(result["data"], list) else result["data"]
    return created


@router.get("/", response_model=List[UserSchema])
def get_accounts(
    user_id: Optional[int] = Query(None),
    email: Optional[str] = Query(None),
    username: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    membership_plan_id: Optional[int] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    """
    Retrieve user accounts with optional filtering and pagination.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "GET_ACCOUNT",
                [user_id, email, username, status, membership_plan_id, page, limit],
            )
            result = cur.fetchone()
            data = result["data"] if result and "data" in result else []
    return data


@router.patch("/{user_id}", response_model=UserSchema)
def patch_account(user_id: int, data: UserCreateSchema = Body(...)):
    """
    Partially update a user account.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PATCH_ACCOUNT",
                [
                    user_id,
                    data.email,
                    data.username,
                    data.hashed_password,
                    data.avatar_url,
                    data.status,
                ],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"User {user_id} not found")
            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]
    return updated


@router.put("/{user_id}", response_model=UserSchema)
def put_account(user_id: int, data: UserCreateSchema):
    """
    Fully update a user account.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PUT_ACCOUNT",
                [
                    user_id,
                    data.email,
                    data.username,
                    data.hashed_password,
                    data.avatar_url,
                    data.status,
                ],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"User {user_id} not found")
            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]
    return updated


@router.delete("/{user_id}")
def delete_account(user_id: int):
    """
    Delete a user account.
    Returns success status.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("DELETE_ACCOUNT", [user_id])
            result = cur.fetchone()
            if not result or "success" not in result:
                raise HTTPException(status_code=404, detail=f"User {user_id} not found")
            return {"success": result["success"]}
