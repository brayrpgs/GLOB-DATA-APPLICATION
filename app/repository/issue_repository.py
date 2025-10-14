from asyncpg import Pool
from typing import Optional, List, Dict, Any,Union
from datetime import date
from app.schemas.issue import IssueCreate, IssuePatchRequest, IssuePutRequest
import json
import logging

logger = logging.getLogger(__name__)


class IssueRepository:
    """Repository to handle data access logic for Issues"""

    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def post_issue(self, issue: IssueCreate) -> Dict[str, Any]:
        query = 'CALL PUBLIC."POST_ISSUE"($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    query,
                    issue.summary,
                    issue.description,
                    issue.resolve_at,
                    issue.due_date,
                    issue.votes,
                    issue.original_estimation,
                    issue.custom_start_date,
                    issue.story_point_estimate,
                    issue.parent_summary,
                    issue.issue_type,
                    issue.project_id,
                    issue.user_assigned,
                    issue.user_creator,
                    issue.user_informator,
                    issue.sprint_id,
                    issue.status
                )
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error in post_issue: %s", e)
            raise

    async def get_issues(
        self,
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
    ) -> List[Dict[str, Any]]:
        query = 'CALL PUBLIC."GET_ISSUE"(NULL, $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    query,
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
                )
                if not row:
                    return []

                data_json = row.get("data")
                data_list = json.loads(data_json) if isinstance(data_json, str) else data_json

                return data_list if data_list else []
        except Exception as e:
            logger.exception("Error in get_issues: %s", e)
            raise

    async def patch_issue(self, issue_id: int, issue: IssuePatchRequest) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PATCH_ISSUE"(NULL, $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    query,
                    issue_id,
                    issue.summary,
                    issue.description,
                    issue.audit_id,
                    issue.resolve_at,
                    issue.due_date,
                    issue.votes,
                    issue.original_estimation,
                    issue.custom_start_date,
                    issue.story_point_estimate,
                    issue.parent_summary,
                    issue.issue_type,
                    issue.project_id,
                    issue.user_assigned,
                    issue.user_creator,
                    issue.user_informator,
                    issue.sprint_id,
                    issue.status
                )
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error in patch_issue: %s", e)
            raise

    async def put_issue(self, issue_id: int, issue: IssuePutRequest) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PUT_ISSUE"($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    query,
                    issue_id,
                    issue.summary,
                    issue.description,
                    issue.audit_id,
                    issue.resolve_at,
                    issue.due_date,
                    issue.votes,
                    issue.original_estimation,
                    issue.custom_start_date,
                    issue.story_point_estimate,
                    issue.parent_summary,
                    issue.issue_type,
                    issue.project_id,
                    issue.user_assigned,
                    issue.user_creator,
                    issue.user_informator,
                    issue.sprint_id,
                    issue.status
                )
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error in put_issue: %s", e)
            raise

    async def delete_issue(self, issue_id: int) -> Dict[str, Any]:
        query = 'CALL PUBLIC."DELETE_ISSUE"($1, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, issue_id)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error in delete_issue: %s", e)
            raise
