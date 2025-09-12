from fastapi import APIRouter, Query, Body, status
from typing import List, Optional
from app.schemas.issue_type import IssueTypeSchema, IssueTypeCreateSchema
from app.controllers.issue_type_controller import (
    get_issue_types,
    create_issue_type,
    put_issue_type,
    patch_issue_type,
    delete_issue_type,
)

router = APIRouter(prefix="/issue-types", tags=["Issue Types"])

@router.get("/", response_model=List[IssueTypeSchema])
def route_get_issue_types(
    issue_type_id: Optional[int] = Query(None),
    status_param: Optional[int] = Query(None, alias="status"),
    priority: Optional[int] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    return get_issue_types(issue_type_id, status_param, priority, page, limit)

@router.post("/", response_model=IssueTypeSchema, status_code=status.HTTP_201_CREATED)
def route_create_issue_type(issue_type: IssueTypeCreateSchema = Body(...)):
    return create_issue_type(issue_type)

@router.put("/{issue_type_id}", response_model=IssueTypeSchema)
def route_put_issue_type(issue_type_id: int, issue_type: IssueTypeCreateSchema = Body(...)):
    return put_issue_type(issue_type_id, issue_type)

@router.patch("/{issue_type_id}", response_model=IssueTypeSchema)
def route_patch_issue_type(issue_type_id: int, issue_type: IssueTypeCreateSchema = Body(...)):
    return patch_issue_type(issue_type_id, issue_type)

@router.delete("/{issue_type_id}", response_model=IssueTypeSchema)
def route_delete_issue_type(issue_type_id: int):
    return delete_issue_type(issue_type_id)
