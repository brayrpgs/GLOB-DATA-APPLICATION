from fastapi import APIRouter, Query, Depends
from asyncpg import Pool
from app.controllers.issue_type_controller import (
    post_issue_type_controller,
    get_issue_type_controller,
    patch_issue_type_controller,
    put_issue_type_controller,
    delete_issue_type_controller
)
from app.database.conection import get_pool
from app.schemas.issue_type import IssueTypeCreate

router = APIRouter(
    prefix="/issue-types",
    tags=["issue-types"]
)

@router.post("/")
async def create_issue_type(
    issue_type: IssueTypeCreate,
    db_pool: Pool = Depends(get_pool)
):
    """Create an issue type by accepting a JSON body matching IssueTypeCreate schema."""
    # Validate required fields
    if issue_type.status is None or issue_type.priority is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="status and priority are required fields")
    # Extract fields from the body and forward to the controller
    return await post_issue_type_controller(db_pool, issue_type.status, issue_type.priority)

@router.get("/")
async def get_issue_types(
    issue_type_id: int = Query(None),
    status: int = Query(None),
    priority: int = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db_pool: Pool = Depends(get_pool)
):
    return await get_issue_type_controller(db_pool, issue_type_id, status, priority, page, limit)

@router.patch("/")
async def patch_issue_type(
    issue_type_id: int = Query(...),
    status: int = Query(None),
    priority: int = Query(None),
    db_pool: Pool = Depends(get_pool)
):
    return await patch_issue_type_controller(db_pool, issue_type_id, status, priority)

@router.put("/")
async def put_issue_type(
    issue_type_id: int = Query(...),
    status: int = Query(...),
    priority: int = Query(...),
    db_pool: Pool = Depends(get_pool)
):
    return await put_issue_type_controller(db_pool, issue_type_id, status, priority)

@router.delete("/{issue_type_id}")
async def delete_issue_type(issue_type_id: int, db_pool: Pool = Depends(get_pool)):
    return await delete_issue_type_controller(db_pool, issue_type_id)
