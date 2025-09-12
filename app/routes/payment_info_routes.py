from fastapi import APIRouter, Query, HTTPException, status, Body
from typing import List, Optional
from datetime import date

from app.database.conection import get_connection
from app.schemas.payment_info import PaymentInfoSchema, PaymentInfoCreateSchema

router = APIRouter(prefix="/payment-info", tags=["Payment Info"])


@router.post("/", response_model=PaymentInfoSchema, status_code=status.HTTP_201_CREATED)
def create_payment_info(payment_info: PaymentInfoCreateSchema):
    """
    Create a new payment info record using POST_PAYMENT_INFO stored procedure.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "POST_PAYMENT_INFO",
                [
                    payment_info.user_id,
                    payment_info.method,
                    payment_info.last_four_digits,
                    payment_info.status,
                    payment_info.next_payment_date,
                ],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=500, detail="PaymentInfo could not be created")

            created = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return created


@router.get("/", response_model=List[PaymentInfoSchema])
def get_payment_infos(
    payment_info_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    method: Optional[int] = Query(None),
    status_param: Optional[int] = Query(None, alias="status"),
    next_payment_date: Optional[date] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    """
    Get payment info records using GET_PAYMENT_INFO stored procedure.
    Supports filtering and pagination.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "GET_PAYMENT_INFO",
                [payment_info_id, user_id, method, status_param, next_payment_date, page, limit],
            )
            result = cur.fetchone()
            data = result["data"] if result and "data" in result else []

    return data


@router.patch("/{payment_info_id}", response_model=PaymentInfoSchema)
def patch_payment_info(payment_info_id: int, payment_info: PaymentInfoCreateSchema = Body(...)):
    """
    Partially update a payment info record using PATCH_PAYMENT_INFO stored procedure.
    Only provided fields are updated.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PATCH_PAYMENT_INFO",
                [
                    payment_info_id,
                    payment_info.user_id,
                    payment_info.method,
                    payment_info.last_four_digits,
                    payment_info.status,
                    payment_info.next_payment_date,
                ],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"PaymentInfo with ID {payment_info_id} not found")

            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return updated


@router.put("/{payment_info_id}", response_model=PaymentInfoSchema)
def put_payment_info(payment_info_id: int, payment_info: PaymentInfoCreateSchema):
    """
    Fully update a payment info record using PUT_PAYMENT_INFO stored procedure.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                "PUT_PAYMENT_INFO",
                [
                    payment_info_id,
                    payment_info.user_id,
                    payment_info.method,
                    payment_info.last_four_digits,
                    payment_info.status,
                    payment_info.next_payment_date,
                ],
            )
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"PaymentInfo with ID {payment_info_id} not found")

            updated = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return updated


@router.delete("/{payment_info_id}", response_model=PaymentInfoSchema)
def delete_payment_info(payment_info_id: int):
    """
    Delete a payment info record using DELETE_PAYMENT_INFO stored procedure.
    Returns the deleted record.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("DELETE_PAYMENT_INFO", [payment_info_id])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"PaymentInfo with ID {payment_info_id} not found")

            deleted = result["data"][0] if isinstance(result["data"], list) else result["data"]

    return deleted
