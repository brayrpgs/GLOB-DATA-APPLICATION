from asyncpg import Pool
from typing import List, Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

class AccountRepository:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def post_account(
        self,
        email: str,
        username: str,
        hashed_password: str,
        avatar_url: str,
        status: int
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."POST_ACCOUNT"($1, $2, $3, $4, $5, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, email, username, hashed_password, avatar_url, status)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en post_account: %s", e)
            raise

    async def get_account(
        self,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        username: Optional[str] = None,
        status: Optional[int] = None,
        membership_plan_id: Optional[int] = None,
        page: int = 1,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        query = 'CALL PUBLIC."GET_ACCOUNT"(NULL, $1, $2, $3, $4, $5, $6, $7)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_id, email, username, status, membership_plan_id, page, limit)
                if not row:
                    return []

                # Extract OUT parameter DATA JSON
                data_json = row.get("data")
                data_list = json.loads(data_json) if isinstance(data_json, str) else data_json
                
                return data_list if data_list is not None else []
        except Exception as e:
            logger.exception("Error en get_account: %s", e)
            raise

    async def patch_account(
        self,
        user_id: int,
        email: Optional[str] = None,
        username: Optional[str] = None,
        hashed_password: Optional[str] = None,
        avatar_url: Optional[str] = None,
        status: Optional[int] = None
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PATCH_ACCOUNT"(NULL, $1, $2, $3, $4, $5, $6)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_id, email, username, hashed_password, avatar_url, status)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en patch_account: %s", e)
            raise

    async def put_account(
        self,
        user_id: int,
        email: str,
        username: str,
        hashed_password: str,
        avatar_url: str,
        status: int
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PUT_ACCOUNT"(NULL, $1, $2, $3, $4, $5, $6)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_id, email, username, hashed_password, avatar_url, status)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en put_account: %s", e)
            raise

    async def delete_account(self, user_id: int) -> bool:
        query = 'CALL PUBLIC."DELETE_ACCOUNT"($1, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_id)
                if not row:
                    return False
                # The SP returns SUCCESS BOOLEAN instead of DATA JSON
                success = row.get("success") if "success" in row else row[0]
                return bool(success) if success is not None else False
        except Exception as e:
            logger.exception("Error en delete_account: %s", e)
            raise