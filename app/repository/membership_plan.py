from asyncpg import Pool
from typing import List, Dict, Any, Optional
import json
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class MembershipPlanRepository:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def post_membership_plan(
        self,
        name: str,
        description: str,
        amount: Decimal
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."POST_MEMBERSHIP_PLAN"($1, $2, $3, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, name, description, amount)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en post_membership_plan: %s", e)
            raise

    async def get_membership_plan(
        self,
        membershipplan_id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[Decimal] = None,
        page: int = 1,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        query = 'CALL PUBLIC."GET_MEMBERSHIP_PLAN"(NULL, $1, $2, $3, $4, $5, $6)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, membershipplan_id, name, description, amount, page, limit)
                if not row:
                    return []

                # Extraer OUT parameter DATA JSON
                data_json = row.get("data")
                data_list = json.loads(data_json) if isinstance(data_json, str) else data_json
                
                return data_list if data_list is not None else []
        except Exception as e:
            logger.exception("Error en get_membership_plan: %s", e)
            raise

    async def patch_membership_plan(
        self,
        membershipplan_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        amount: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PATCH_MEMBERSHIP_PLAN"(NULL, $1, $2, $3, $4)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, membershipplan_id, name, description, amount)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en patch_membership_plan: %s", e)
            raise
    async def put_membership_plan(
        self,
        membershipplan_id: int,
        name: str,
        description: str,
        amount: Decimal
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PUT_MEMBERSHIP_PLAN"($1, $2, $3, $4, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, membershipplan_id, name, description, amount)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en put_membership_plan: %s", e)
            raise

    async def delete_membership_plan(self, membershipplan_id: int) -> bool:
        query = 'CALL PUBLIC."DELETE_MEMBERSHIP_PLAN"($1, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, membershipplan_id)
                if not row:
                    return False
                # El SP retorna SUCCESS BOOLEAN en lugar de DATA JSON
                success = row.get("success") if "success" in row else row[0]
                return bool(success) if success is not None else False
        except Exception as e:
            logger.exception("Error en delete_membership_plan: %s", e)
            raise