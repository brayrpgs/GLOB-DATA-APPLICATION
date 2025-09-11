from fastapi import APIRouter, Query
from schemas import Item
from typing import List,Optional
from database import conection  # tu archivo con get_connection
from schemas import IssueSchema
router = APIRouter()
router = APIRouter(prefix="/issues", tags=["Issues"])
@router.get("/")
def read_root():
    return {"message": "Hello from items router"}

@router.get("/items", response_model=List[Item])
def read_items():
    return [
        {"id": 1, "name": "Item 1", "description": "This is item 1"},
        {"id": 2, "name": "Item 2", "description": "This is item 2"},
    ]
@router.get("/", response_model=List[IssueSchema])
def get_issues(
    issue_id: Optional[int] = Query(None),
    summary: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    audit_id: Optional[int] = Query(None),
    resolve_at: Optional[str] = Query(None),
    due_date: Optional[str] = Query(None),
    votes: Optional[int] = Query(None),
    original_estimation: Optional[int] = Query(None),
    custom_start_date: Optional[str] = Query(None),
    story_point_estimate: Optional[int] = Query(None),
    parent_summary: Optional[int] = Query(None),
    issue_type: Optional[int] = Query(None),
    project_id_fk: Optional[int] = Query(None),
    user_assigned_fk: Optional[int] = Query(None),
    user_creator_issue_fk: Optional[int] = Query(None),
    user_informator_fk: Optional[int] = Query(None),
    sprint_id_fk: Optional[int] = Query(None),
    status_issue: Optional[int] = Query(None),
    page: int = Query(1),
    limit: int = Query(10),
):
    """
    Llama al SP GET_ISSUE para obtener una lista de issues filtrada y paginada.
    """

    with conection() as conn:
        with conn.cursor() as cur:
            cur.callproc(
                'GET_ISSUE',
                [
                    issue_id,
                    summary,
                    description,
                    audit_id,
                    resolve_at,
                    due_date,
                    votes,
                    original_estimation,
                    custom_start_date,
                    story_point_estimate,
                    parent_summary,
                    issue_type,
                    project_id_fk,
                    user_assigned_fk,
                    user_creator_issue_fk,
                    user_informator_fk,
                    sprint_id_fk,
                    status_issue,
                    page,
                    limit
                ]
            )

            result = cur.fetchone()  # SP devuelve OUT DATA (JSON)
            data = result["data"] if result and "data" in result else []

    return data