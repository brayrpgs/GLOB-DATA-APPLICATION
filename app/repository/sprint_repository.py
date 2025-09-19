from datetime import date
import json
import logging
from typing import Optional, Dict, Any
from asyncpg import Pool

logger = logging.getLogger(__name__)

class SprintRepository:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def get_sprint(
        self,
        sprint_id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        date_init_start: Optional[str] = None,
        date_init_end: Optional[str] = None,
        date_end_start: Optional[str] = None,
        date_end_end: Optional[str] = None,
        page: int = 1,
        limit: int = 10,
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."GET_SPRINT"(NULL, $1, $2, $3, $4, $5, $6, $7, $8, $9)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    query,
                    sprint_id,
                    name,
                    description,
                    date_init_start,
                    date_init_end,
                    date_end_start,
                    date_end_end,
                    page,
                    limit
                )
                if not row or row.get("data") is None:
                    return {"data": [], "page": page, "currentLimit": limit, "totalData": 0}

                data_json = row["data"]
                data_list = json.loads(data_json) if isinstance(data_json, str) else data_json

                return {
                    "data": data_list,
                    "page": page,
                    "currentLimit": limit,
                    "totalData": len(data_list)
                }
        except Exception as e:
            logger.exception("Error en get_sprint: %s", e)
            raise

    async def post_sprint(self, params: tuple) -> Dict[str, Any]:
        query = f'CALL PUBLIC."POST_SPRINT"({",".join([f"${i+1}" for i in range(len(params))])}, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, *params)
                if not row:
                    return {}
                data_json = row.get("data")
                return json.loads(data_json) if isinstance(data_json, str) else data_json
        except Exception as e:
            logger.exception("Error en post_sprint: %s", e)
            raise

    async def patch_sprint(
        self,
        sprint_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        date_init: Optional[date] = None,
        date_end: Optional[date] = None
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PATCH_SPRINT"(NULL, $1, $2, $3, $4, $5)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, sprint_id, name, description, date_init, date_end)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en patch_sprint: %s", e)
            raise

    async def put_sprint(
        self,
        sprint_id: int,
        name: str,
        description: str,
        date_init: date,
        date_end: date
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PUT_SPRINT"($1, $2, $3, $4, $5, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, sprint_id, name, description, date_init, date_end)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en put_sprint: %s", e)
            raise

    async def delete_sprint(self, sprint_id: int) -> Dict[str, Any]:
        query = 'CALL PUBLIC."DELETE_SPRINT"($1, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, sprint_id)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en delete_sprint: %s", e)
            raise