from typing import Any
from fastapi import APIRouter, Body, HTTPException, Depends, Path
from asyncpg import Pool
from app.database.conection import get_pool
from app.schemas.membership import membership

router = APIRouter(
    prefix="/membership",
    tags=["membership"]
)

@router.patch("/{user_id}")
async def membership_patch(
    body: membership = Body(...),
    user_id: int = Path(..., description="ID of the user to patch"),
    db_pool: Pool = Depends(get_pool)
):
    query = """
        UPDATE public."USER"
        SET "MEMBERSHIP_PLAN_ID" = $1
        WHERE "USER_ID" = $2
        RETURNING "USER_ID", "MEMBERSHIP_PLAN_ID";
    """

    async with db_pool.acquire() as connection:
        result = await connection.fetchrow(query, body.membership, user_id)

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "message": "Membership updated successfully",
        "user": dict(result)
    }
