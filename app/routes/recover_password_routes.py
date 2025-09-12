from fastapi import APIRouter, HTTPException, status, Body, Query
from typing import List, Optional
from datetime import date

from app.database.conection import get_connection
from app.schemas.recover_password import RecoverPasswordSchema, RecoverPasswordCreateSchema

router = APIRouter(prefix="/recover-password", tags=["Recover Password"])


@router.post("/", response_model=RecoverPasswordSchema, status_code=status.HTTP_201_CREATED)
def create_recover_password(data: RecoverPasswordCreateSchema):
    """
    Create a new recover password record.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "POST_RECOVER_PASSWORD",
                [data.user_id, data.otp, data.is_used, data.expiry_date],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=500, detail="RecoverPassword could not be created")
            created = result["data"][0] if isinstance(result["data"], list) else result["data"]
    return created


@router.get("/", response_model=List[RecoverPasswordSchema])
def get_recover_passwords(
    recover_password_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    otp: Optional[str] = Query(None),
    is_used: Optional[bool] = Query(None),
    expiry_date: Optional[date] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    """
    Retrieve recover password records with optional filtering and pagination.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "GET_RECOVER_PASSWORD",
                [recover_password_id, user_id, otp, is_used, expiry_date, page, limit],
            )
            result = cur.fetchone()
            data = result["data"] if result and "data" in result else []
    return data


@router.patch("/{recover_password_id}", response_model=RecoverPasswordSchema)
def patch_recover_password(recover_password_id: int, data: RecoverPasswordCreateSchema = Body(...)):
    """
    Partially update a recover password record.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PATCH_RECOVER_PASSWORD",
                [recover_password_id, data.user_id, data.otp, data.is_used, data.expiry_date],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"RecoverPassword {recover_password_id} not found")
            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]
    return updated


@router.put("/{recover_password_id}", response_model=RecoverPasswordSchema)
def put_recover_password(recover_password_id: int, data: RecoverPasswordCreateSchema):
    """
    Fully update a recover password record.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PUT_RECOVER_PASSWORD",
                [recover_password_id, data.user_id, data.otp, data.is_used, data.expiry_date],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"RecoverPassword {recover_password_id} not found")
            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]
    return updated


@router.delete("/{recover_password_id}", response_model=RecoverPasswordSchema)
def delete_recover_password(recover_password_id: int):
    """
    Delete a recover password record.
    Returns the deleted record.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("DELETE_RECOVER_PASSWORD", [recover_password_id])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"RecoverPassword {recover_password_id} not found")
            deleted = result["data"][0] if isinstance(result["data"], list) else result["data"]
    return deleted
