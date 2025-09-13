from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.issue import Issue
import logging

# Configurar logger para el schema
logger = logging.getLogger(__name__)


class IssueSchema(BaseModel):
    issue_id: Optional[int] = Field(None, alias="ISSUE_ID")
    summary: Optional[str] = Field(None, alias="SUMMARY")
    description: Optional[str] = Field(None, alias="DESCRIPTION")
    audit_id_fk: Optional[int] = Field(None, alias="AUDIT_ID_FK")
    resolve_at: Optional[str] = Field(None, alias="RESOLVE_AT")
    due_date: Optional[str] = Field(None, alias="DUE_DATE")
    votes: Optional[int] = Field(None, alias="VOTES")
    original_estimation: Optional[int] = Field(None, alias="ORIGINAL_ESTIMATION")
    custom_start_date: Optional[str] = Field(None, alias="CUSTOM_START_DATE")
    story_point_estimate: Optional[int] = Field(None, alias="STORY_POINT_ESTIMATE")
    parent_summary_fk: Optional[int] = Field(None, alias="PARENT_SUMMARY_FK")
    issue_type: Optional[int] = Field(None, alias="ISSUE_TYPE")
    project_id_fk: Optional[int] = Field(None, alias="PROJECT_ID_FK")
    user_assigned_fk: Optional[int] = Field(None, alias="USER_ASSIGNED_FK")
    user_creator_issue_fk: Optional[int] = Field(None, alias="USER_CREATOR_ISSUE_FK")
    # Corregido para que coincida con el JSON del SP
    user_informator_issue_fk: Optional[int] = Field(None, alias="USER_INFORMATOR_ISSUE_FK")
    sprint_id_fk: Optional[int] = Field(None, alias="SPRINT_ID_FK")
    status_issue: Optional[int] = Field(None, alias="STATUS_ISSUE")

    class Config:
        allow_population_by_field_name = True


class IssueResponse(BaseModel):
    """
    Respuesta que contiene la lista de issues.
    El SP devuelve un JSON array que se parsea directamente.
    """
    data: List[Dict[str, Any]]  # JSON raw del SP
    
    # Método para convertir a lista de Issues validados
    def get_validated_issues(self) -> List[Issue]:
        """Convierte los datos raw a objetos Issue validados"""
        validated_issues = []
        for item in self.data:
            try:
                # Convertir fechas de string a date si es necesario
                issue_data = item.copy()
                date_fields = ['RESOLVE_AT', 'DUE_DATE', 'CUSTOM_START_DATE']
                for field in date_fields:
                    if field in issue_data and isinstance(issue_data[field], str):
                        try:
                            from datetime import datetime
                            issue_data[field] = datetime.strptime(issue_data[field], '%Y-%m-%d').date()
                        except:
                            issue_data[field] = None
                
                validated_issues.append(Issue(**issue_data))
            except Exception as e:
                logger.warning("Error al validar issue: %s, data: %s", e, item)
                continue
        return validated_issues


class IssueResponseValidated(BaseModel):
    """
    Versión que valida directamente como Issues (más estricta)
    """
    data: List[Issue]
    
    @classmethod
    def from_raw_response(cls, raw_data: List[Dict[str, Any]]):
        """Crear desde datos raw del SP"""
        validated_issues = []
        for item in raw_data:
            try:
                validated_issues.append(Issue(**item))
            except Exception as e:
                logger.warning("Error al validar issue: %s", e)
                continue
        return cls(data=validated_issues)