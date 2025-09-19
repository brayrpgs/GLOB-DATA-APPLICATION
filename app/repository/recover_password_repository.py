from asyncpg import Pool
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import date

logger = logging.getLogger(__name__)

class RecoverPasswordRepository:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def post_recover_password(
        self,
        user_id: int,
        otp: str,
        is_used: int,
        expiry_date: date
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."POST_RECOVER_PASSWORD"($1, $2, $3, $4, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_id, otp, is_used, expiry_date)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en post_recover_password: %s", e)
            raise

    async def get_recover_password(
        self,
        recover_password_id: Optional[int] = None,
        user_id: Optional[int] = None,
        otp: Optional[str] = None,
        is_used: Optional[int] = None,
        expiry_date: Optional[date] = None,
        page: int = 1,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        query = 'CALL PUBLIC."GET_RECOVER_PASSWORD"(NULL, $1, $2, $3, $4, $5, $6, $7)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, recover_password_id, user_id, otp, is_used, expiry_date, page, limit)
                if not row:
                    return []

                # Extract OUT parameter DATA JSON
                data_json = row.get("data")
                data_list = json.loads(data_json) if isinstance(data_json, str) else data_json
                
                return data_list if data_list is not None else []
        except Exception as e:
            logger.exception("Error en get_recover_password: %s", e)
            raise

    async def patch_recover_password(
        self,
        recover_password_id: int,
        user_id: Optional[int] = None,
        otp: Optional[str] = None,
        is_used: Optional[int] = None,
        expiry_date: Optional[date] = None
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PATCH_RECOVER_PASSWORD"(NULL, $1, $2, $3, $4, $5)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, recover_password_id, user_id, otp, is_used, expiry_date)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en patch_recover_password: %s", e)
            raise

    async def put_recover_password(
        self,
        recover_password_id: int,
        user_id: int,
        otp: str,
        is_used: int,
        expiry_date: date
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PUT_RECOVER_PASSWORD"($1, $2, $3, $4, $5, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, recover_password_id, user_id, otp, is_used, expiry_date)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en put_recover_password: %s", e)
            raise

    async def delete_recover_password(self, recover_password_id: int) -> Dict[str, Any]:
        query = 'CALL PUBLIC."DELETE_RECOVER_PASSWORD"($1, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, recover_password_id)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en delete_recover_password: %s", e)
            raise