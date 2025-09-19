from asyncpg import Pool
from typing import List, Dict, Any, Optional
import json
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class UserProjectRepository:
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def post_user_project(
        self,
        user_id_fk: int,
        rol_proyect: int,
        productivity: Decimal
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."POST_USER_PROJECT"($1, $2, $3, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_id_fk, rol_proyect, productivity)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en post_user_project: %s", e)
            raise

    async def get_user_project(
        self,
        user_project_id: Optional[int] = None,
        user_id_fk: Optional[int] = None,
        rol_proyect: Optional[int] = None,
        productivity: Optional[Decimal] = None,
        page: int = 1,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        query = 'CALL PUBLIC."GET_USER_PROJECT"(NULL, $1, $2, $3, $4, $5, $6)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_project_id, user_id_fk, rol_proyect, productivity, page, limit)
                if not row:
                    return []

                # Extraer OUT parameter DATA JSON
                data_json = row.get("data")
                data_list = json.loads(data_json) if isinstance(data_json, str) else data_json
                
                return data_list if data_list is not None else []
        except Exception as e:
            logger.exception("Error en get_user_project: %s", e)
            raise

    async def patch_user_project(
        self,
        user_project_id: int,
        user_id_fk: Optional[int] = None,
        rol_proyect: Optional[int] = None,
        productivity: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PATCH_USER_PROJECT"(NULL, $1, $2, $3, $4)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_project_id, user_id_fk, rol_proyect, productivity)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en patch_user_project: %s", e)
            raise

    async def put_user_project(
        self,
        user_project_id: int,
        user_id_fk: int,
        rol_proyect: int,
        productivity: Decimal
    ) -> Dict[str, Any]:
        query = 'CALL PUBLIC."PUT_USER_PROJECT"($1, $2, $3, $4, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_project_id, user_id_fk, rol_proyect, productivity)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en put_user_project: %s", e)
            raise

    async def delete_user_project(self, user_project_id: int) -> Dict[str, Any]:
        query = 'CALL PUBLIC."DELETE_USER_PROJECT"($1, NULL)'
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(query, user_project_id)
                if not row:
                    return {}
                result_data = row.get("data") if "data" in row else row[0]
                return json.loads(result_data) if isinstance(result_data, str) else result_data
        except Exception as e:
            logger.exception("Error en delete_user_project: %s", e)
            raise