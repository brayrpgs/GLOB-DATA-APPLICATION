from fastapi import HTTPException
from asyncpg import Pool
from typing import Optional
from app.schemas.issue import IssueResponse
from app.repository.issue_repository import IssueRepository
import logging
from app.helpers.utilities import _validate_pagination_parameters

logger = logging.getLogger(__name__)


async def post_issue_controller(db_pool: Optional[Pool], issue_data: dict) -> dict:
    if db_pool is None:
        raise HTTPException(status_code=500, detail="DB pool no inicializado")

    try:
        repo = IssueRepository(db_pool)

        params = (
            issue_data.get("summary"),
            issue_data.get("description"),
            issue_data.get("resolve_at"),
            issue_data.get("due_date"),
            issue_data.get("votes"),
            issue_data.get("original_estimation"),
            issue_data.get("custom_start_date"),
            issue_data.get("story_point_estimate"),
            issue_data.get("parent_summary"),
            issue_data.get("issue_type"),
            issue_data.get("project_id"),
            issue_data.get("user_assigned"),
            issue_data.get("user_creator"),
            issue_data.get("user_informator"),
            issue_data.get("sprint_id"),
            issue_data.get("status"),
            None  # OUT param DATA
        )

        new_issue = await repo.post_issue(params)
        return {"data": new_issue}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

async def get_issues_controller(
    db_pool: Optional[Pool],
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
    limit: int = 10,
) -> IssueResponse:
    # Validar pool de conexiones
    if db_pool is None:
        logger.error("DB pool no inicializado")
        raise HTTPException(status_code=500, detail="DB pool no inicializado")

    # Validaciones de negocio
    _validate_pagination_parameters(page, limit)

    try:
        # Crear repository e inyectar dependencias
        issue_repository = IssueRepository(db_pool)

        # Obtener datos del repository
        issues_data = await issue_repository.get_issues(
            issue_id=issue_id,
            summary=summary,
            description=description,
            audit_id=audit_id,
            resolve_at=resolve_at,
            due_date=due_date,
            votes=votes,
            original_estimation=original_estimation,
            custom_start_date=custom_start_date,
            story_point_estimate=story_point_estimate,
            parent_summary=parent_summary,
            issue_type=issue_type,
            project_id_fk=project_id_fk,
            user_assigned_fk=user_assigned_fk,
            user_creator_issue_fk=user_creator_issue_fk,
            user_informator_fk=user_informator_fk,
            sprint_id_fk=sprint_id_fk,
            status_issue=status_issue,
            page=page,
            limit=limit,
        )

        # Retornar respuesta estructurada
        return IssueResponse(
            data=issues_data, page=page, currentLimit=limit, totalData=len(issues_data)
        )

    except HTTPException:
        # Re-lanzar HTTPExceptions sin modificar
        raise

    except Exception as e:
        # Capturar errores inesperados y convertir a HTTPException
        logger.exception("Error inesperado en get_issues_controller")
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}"
        )


async def delete_issue_controller(db_pool: Optional[Pool], issue_id: int) -> dict:
    if db_pool is None:
        logger.error("DB pool no inicializado")
        raise HTTPException(status_code=500, detail="DB pool no inicializado")

    try:
        issue_repository = IssueRepository(db_pool)
        deleted_issue = await issue_repository.delete_issue(issue_id)

        if not deleted_issue:
            raise HTTPException(status_code=404, detail="Issue no encontrado")

        return {"data": deleted_issue}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error inesperado en delete_issue_controller")
        raise HTTPException(
            status_code=500, detail=f"Error interno del servidor: {str(e)}"
        )
