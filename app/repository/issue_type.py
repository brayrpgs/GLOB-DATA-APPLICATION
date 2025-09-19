from asyncpg import Pool
from typing import List, Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

class IssueTypeRepository:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def post_issue_type(self, status: int, priority: int) -> Dict[str, Any]:
        query = 'CALL PUBLIC."POST_ISSUE_TYPE"($1, $2, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, status, priority)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en post_issue_type: %s", e)
            raise

    async def get_issue_type(
        self,
        issue_type_id: Optional[int] = None,
        status: Optional[int] = None,
        priority: Optional[int] = None,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:  # <- returns dict with data, page, etc.
        query = 'CALL PUBLIC."GET_ISSUE_TYPE"(NULL, $1, $2, $3, $4, $5)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, issue_type_id, status, priority, page, limit)
                if not row:
                    return {}

                # Extract OUT parameter DATA JSON
                data_json = row.get("data")
                data_list = json.loads(data_json) if isinstance(data_json, str) else data_json

                return {"data": data_list}
        except Exception as e:
            logger.exception("Error en get_issue_type: %s", e)
            raise

    async def patch_issue_type(self, issue_type_id: int, status: Optional[int] = None, priority: Optional[int] = None) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PATCH_ISSUE_TYPE"(NULL, $1, $2, $3)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, issue_type_id, status, priority)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en patch_issue_type: %s", e)
            raise

    async def put_issue_type(self, issue_type_id: int, status: int, priority: int) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PUT_ISSUE_TYPE"($1, $2, $3, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, issue_type_id, status, priority)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en put_issue_type: %s", e)
            raise

    async def delete_issue_type(self, issue_type_id: int) -> Dict[str, Any]:
        query = 'CALL PUBLIC."DELETE_ISSUE_TYPE"($1, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, issue_type_id)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en delete_issue_type: %s", e)
            raise
