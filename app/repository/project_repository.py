from datetime import date
from decimal import Decimal
from asyncpg import Pool
from typing import Dict, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)

class ProjectRepository:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def post_project(
        self,
        name: str,
        description: str,
        date_init: date,
        date_end: date,
        status: int,
        progress: Decimal,
        user_project_id_fk: Optional[int] = None
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."POST_PROJECT"($1, $2, $3, $4, $5, $6, $7, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, name, description, date_init, date_end, status, progress, user_project_id_fk)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en post_project: %s", e)
            raise

        
    async def get_project(
        self,
        project_id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        user_project_id_fk: Optional[int] = None,
        date_init_start: Optional[str] = None,
        date_init_end: Optional[str] = None,
        date_end_start: Optional[str] = None,
        date_end_end: Optional[str] = None,
        status: Optional[int] = None,
        progress_min: Optional[float] = None,
        progress_max: Optional[float] = None,
        page: int = 1,
        limit: int = 10
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."GET_PROJECT"(NULL,$1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    query,
                    project_id, name, description, user_project_id_fk,
                    date_init_start, date_init_end, date_end_start, date_end_end,
                    status, progress_min, progress_max, page, limit
                )
                if not row:
                    return {"data": []}
                return {"data": json.loads(row["data"])}
        except Exception as e:
            logger.exception("Error en get_project: %s", e)
            raise

    async def patch_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        user_project_id_fk: Optional[int] = None,
        date_init: Optional[date] = None,
        date_end: Optional[date] = None,
        status: Optional[int] = None,
        progress: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PATCH_PROJECT"(NULL, $1, $2, $3, $4, $5, $6, $7, $8)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, project_id, name, description, user_project_id_fk, date_init, date_end, status, progress)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en patch_project: %s", e)
            raise

    async def put_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        user_project_id_fk: Optional[int] = None,
        date_init: Optional[date] = None,
        date_end: Optional[date] = None,
        status: Optional[int] = None,
        progress: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PUT_PROJECT"($1, $2, $3, $4, $5, $6, $7, $8, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, project_id, name, description, user_project_id_fk, date_init, date_end, status, progress)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en put_project: %s", e)
            raise

    async def delete_project(self, project_id: int) -> Dict[str, Any]:
        query = 'CALL PUBLIC."DELETE_PROJECT"($1,NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, project_id)
                if not row:
                    return {}
                return json.loads(row["data"]) if "data" in row else row
        except Exception as e:
            logger.exception("Error en delete_project: %s", e)
            raise
