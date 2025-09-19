from asyncpg import Pool
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import date

logger = logging.getLogger(__name__)

class PaymentInfoRepository:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def post_payment_info(
        self,
        user_id: int,
        method: int,
        last_four_digits: str,
        status: int,
        next_payment_date: date
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."POST_PAYMENT_INFO"($1, $2, $3, $4, $5, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_id, method, last_four_digits, status, next_payment_date)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en post_payment_info: %s", e)
            raise

    async def get_payment_info(
        self,
        payment_info_id: Optional[int] = None,
        user_id: Optional[int] = None,
        method: Optional[int] = None,
        status: Optional[int] = None,
        next_payment_date: Optional[date] = None,
        page: int = 1,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        query = 'CALL PUBLIC."GET_PAYMENT_INFO"(NULL, $1, $2, $3, $4, $5, $6, $7)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, payment_info_id, user_id, method, status, next_payment_date, page, limit)
                if not row:
                    return []

                # Extract OUT parameter DATA JSON
                data_json = row.get("data")
                data_list = json.loads(data_json) if isinstance(data_json, str) else data_json
                
                return data_list if data_list is not None else []
        except Exception as e:
            logger.exception("Error en get_payment_info: %s", e)
            raise

    async def patch_payment_info(
        self,
        payment_info_id: int,
        user_id: Optional[int] = None,
        method: Optional[int] = None,
        last_four_digits: Optional[str] = None,
        status: Optional[int] = None,
        next_payment_date: Optional[date] = None
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PATCH_PAYMENT_INFO"(NULL, $1, $2, $3, $4, $5, $6)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, payment_info_id, user_id, method, last_four_digits, status, next_payment_date)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en patch_payment_info: %s", e)
            raise

    async def put_payment_info(
        self,
        payment_info_id: int,
        user_id: int,
        method: int,
        last_four_digits: str,
        status: int,
        next_payment_date: date
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PUT_PAYMENT_INFO"($1, $2, $3, $4, $5, $6, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, payment_info_id, user_id, method, last_four_digits, status, next_payment_date)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en put_payment_info: %s", e)
            raise

    async def delete_payment_info(self, payment_info_id: int) -> Dict[str, Any]:
        query = 'CALL PUBLIC."DELETE_PAYMENT_INFO"($1, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, payment_info_id)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en delete_payment_info: %s", e)
            raise