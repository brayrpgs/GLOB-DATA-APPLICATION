from asyncpg import Pool
from typing import Optional, List, Dict, Any
import json
import logging
from app.helpers.utilities import parse_date

logger = logging.getLogger(__name__)


class IssueRepository:
    """Repository para manejar la lógica de acceso a datos de Issues"""
    
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool
    
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
        """
        Ejecuta el stored procedure GET_ISSUE y retorna los datos parseados.
        
        Returns:
            List[Dict[str, Any]]: Lista de issues obtenidas del SP
            
        Raises:
            Exception: Si hay errores en la ejecución del SP o parsing de datos
        """
        logger.debug("Ejecutando get_issues en repository")
        
        # Preparar parámetros para el SP (21 parámetros total)
        params = self._prepare_sp_parameters(
            issue_id, summary, description, audit_id, resolve_at, due_date,
            votes, original_estimation, custom_start_date, story_point_estimate,
            parent_summary, issue_type, project_id_fk, user_assigned_fk,
            user_creator_issue_fk, user_informator_fk, sprint_id_fk,
            status_issue, page, limit
        )
        
        logger.debug("Parámetros preparados para SP: %s", params)
        
        try:
            async with self.db_pool.acquire() as conn:
                # Ejecutar stored procedure
                row = await self._execute_stored_procedure(conn, params)
                
                # Procesar resultado
                return self._process_sp_result(row)
                
        except Exception as e:
            logger.exception("Error al ejecutar get_issues en repository: %s", str(e))
            raise
    
    def _prepare_sp_parameters(self, *args) -> tuple:
        """
        Prepara los parámetros para el stored procedure GET_ISSUE.
        
        Args:
            *args: Todos los parámetros del método get_issues
            
        Returns:
            tuple: Tupla con los 21 parámetros para el SP
        """
        (issue_id, summary, description, audit_id, resolve_at, due_date,
         votes, original_estimation, custom_start_date, story_point_estimate,
         parent_summary, issue_type, project_id_fk, user_assigned_fk,
         user_creator_issue_fk, user_informator_fk, sprint_id_fk,
         status_issue, page, limit) = args
        
        return (
            None,                           # OUT data (se inicializa en null::json)
            issue_id,                       # P_ISSUE_ID
            summary,                        # P_SUMMARY
            description,                    # P_DESCRIPTION
            audit_id,                       # P_AUDIT_ID
            parse_date(resolve_at),         # P_RESOLVE_AT
            parse_date(due_date),           # P_DUE_DATE
            votes,                          # P_VOTES
            original_estimation,            # P_ORIGINAL_ESTIMATION
            parse_date(custom_start_date),  # P_CUSTOM_START_DATE
            story_point_estimate,           # P_STORY_POINT_ESTIMATE
            parent_summary,                 # P_PARENT_SUMMARY
            issue_type,                     # P_ISSUE_TYPE
            project_id_fk,                  # P_PROJECT_ID_FK
            user_assigned_fk,               # P_USER_ASSIGNED_FK
            user_creator_issue_fk,          # P_USER_CREATOR_ISSUE_FK
            user_informator_fk,             # P_USER_INFORMATOR_FK
            sprint_id_fk,                   # P_SPRINT_ID_FK
            status_issue,                   # P_STATUS_ISSUE
            page,                           # P_PAGE
            limit                           # P_LIMIT
        )
    
    async def _execute_stored_procedure(self, conn, params: tuple):
        """
        Ejecuta el stored procedure GET_ISSUE.
        
        Args:
            conn: Conexión a la base de datos
            params: Parámetros para el SP
            
        Returns:
            Row result del SP
        """
        placeholders = ','.join(f"${i+1}" for i in range(len(params)))
        query = f'CALL PUBLIC."GET_ISSUE"({placeholders})'
        logger.debug("Query a ejecutar: %s", query)
        
        row = await conn.fetchrow(query, *params)
        logger.debug("Resultado del SP: %s", row)
        
        return row
    
    def _process_sp_result(self, row) -> List[Dict[str, Any]]:
        """
        Procesa el resultado del stored procedure.
        
        Args:
            row: Fila resultado del SP
            
        Returns:
            List[Dict[str, Any]]: Lista de issues procesadas
        """
        if not row:
            logger.warning("El SP no devolvió ningún resultado")
            return []
        
        # Extraer el parámetro OUT 'data'
        result_data = row.get('data') if 'data' in row else row[0]
        logger.debug("OUT parameter 'data': %s", result_data)
        
        if result_data is None:
            logger.warning("El parámetro 'data' está vacío")
            return []
        
        # Parsear JSON
        try:
            issues_data = (
                json.loads(result_data)
                if isinstance(result_data, str)
                else result_data
            )
            
            if not isinstance(issues_data, list):
                issues_data = [issues_data] if issues_data else []
            
            logger.debug("Issues parseados: %d registros", len(issues_data))
            return issues_data
            
        except json.JSONDecodeError as je:
            logger.error("Error al parsear JSON: %s", je)
            raise Exception(f"Error al procesar datos del SP: {str(je)}")