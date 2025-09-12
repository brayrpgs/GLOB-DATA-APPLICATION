from typing import List, Optional
from fastapi import HTTPException
from app.database.conection import get_connection
from app.schemas.issue_type import IssueTypeSchema, IssueTypeCreateSchema

def get_issue_types(
    issue_type_id: Optional[int] = None,
    status_param: Optional[int] = None,
    priority: Optional[int] = None,
    page: int = 1,
    limit: int = 10,
) -> List[IssueTypeSchema]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("GET_ISSUE_TYPE", [issue_type_id, status_param, priority, page, limit])
            result = cur.fetchone()
            return result["data"] if result and "data" in result else []

def create_issue_type(issue_type: IssueTypeCreateSchema) -> IssueTypeSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("POST_ISSUE_TYPE", [issue_type.status, issue_type.priority])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=500, detail="IssueType could not be created")
            return result["data"][0] if isinstance(result["data"], list) else result["data"]

def put_issue_type(issue_type_id: int, issue_type: IssueTypeCreateSchema) -> IssueTypeSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("PUT_ISSUE_TYPE", [issue_type_id, issue_type.status, issue_type.priority])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"IssueType with ID {issue_type_id} not found")
            return result["data"][0] if isinstance(result["data"], list) else result["data"]

def patch_issue_type(issue_type_id: int, issue_type: IssueTypeCreateSchema) -> IssueTypeSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("PATCH_ISSUE_TYPE", [issue_type_id, issue_type.status, issue_type.priority])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"IssueType with ID {issue_type_id} not found")
            return result["data"][0] if isinstance(result["data"], list) else result["data"]

def delete_issue_type(issue_type_id: int) -> IssueTypeSchema:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.callproc("DELETE_ISSUE_TYPE", [issue_type_id])
            result = cur.fetchone()
            if not result or not result.get("data"):
                raise HTTPException(status_code=404, detail=f"IssueType with ID {issue_type_id} not found")
            return result["data"]
