from typing import Optional, Dict, Any
from fastapi import HTTPException
from asyncpg import Pool
from app.repository.issue_repository import IssueRepository
from app.schemas.issue import IssueCreate, IssuePatchRequest, IssuePutRequest
import logging

logger = logging.getLogger(__name__)


async def post_issue_controller(db_pool: Pool, issue: IssueCreate) -> Dict[str, Any]:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool not available")
    
    repo = IssueRepository(db_pool)
    try:
        return await repo.post_issue(issue)
    except Exception as e:
        logger.exception("Error in post_issue_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


async def get_issue_controller(
    db_pool: Pool,
    issue_id: Optional[int] = None,
    summary: Optional[str] = None,
    description: Optional[str] = None,
    audit_id: Optional[int] = None,
    resolve_at: Optional[str] = None,
    due_date: Optional[str] = None,
    votes: Optional[int] = None,
    original_estimation: Optional[int] = None,
    custom_start_date: Optional[str] = None,
    story_point_estimate: Optional[int] = None,
    parent_summary: Optional[int] = None,
    issue_type: Optional[int] = None,
    project_id_fk: Optional[int] = None,
    user_assigned_fk: Optional[int] = None,
    user_creator_issue_fk: Optional[int] = None,
    user_informator_fk: Optional[int] = None,
    sprint_id_fk: Optional[int] = None,
    status_issue: Optional[int] = None,
    page: int = 1,
    limit: int = 10
) -> Dict[str, Any]:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool not available")
    
    repo = IssueRepository(db_pool)
    try:
        data = await repo.get_issues(
            issue_id, summary, description, audit_id, resolve_at,
            due_date, votes, original_estimation, custom_start_date,
            story_point_estimate, parent_summary, issue_type, project_id_fk,
            user_assigned_fk, user_creator_issue_fk, user_informator_fk,
            sprint_id_fk, status_issue, page, limit
        )
        return {
            "Issues": data,
            "page": page,
            "currentLimit": limit,
            "totalData": len(data)
        }
    except Exception as e:
        logger.exception("Error in get_issue_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


async def patch_issue_controller(
    db_pool: Pool,
    issue_id: int,
    issue: IssuePatchRequest
) -> Dict[str, Any]:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool not available")
    
    repo = IssueRepository(db_pool)
    try:
        return await repo.patch_issue(issue_id, issue)
    except Exception as e:
        logger.exception("Error in patch_issue_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


async def put_issue_controller(
    db_pool: Pool,
    issue_id: int,
    issue: IssuePutRequest
) -> Dict[str, Any]:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool not available")
    
    repo = IssueRepository(db_pool)
    try:
        return await repo.put_issue(issue_id, issue)
    except Exception as e:
        logger.exception("Error in put_issue_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


async def delete_issue_controller(db_pool: Pool, issue_id: int) -> Dict[str, Any]:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool not available")
    
    repo = IssueRepository(db_pool)
    try:
        return await repo.delete_issue(issue_id)
    except Exception as e:
        logger.exception("Error in delete_issue_controller: %s", e)
        raise HTTPException(status_code=500, detail=str(e))