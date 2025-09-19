from numbers import Number
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.issue import Issue
import logging
from datetime import date

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
    user_informator_issue_fk: Optional[int] = Field(
        None, alias="USER_INFORMATOR_ISSUE_FK"
    )
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
    page: int
    currentLimit: int
    totalData: int

    # Método para convertir a lista de Issues validados
    def get_validated_issues(self) -> List[Issue]:
        """Convierte los datos raw a objetos Issue validados"""
        validated_issues = []
        for item in self.data:
            try:
                # Convertir fechas de string a date si es necesario
                issue_data = item.copy()
                date_fields = ["RESOLVE_AT", "DUE_DATE", "CUSTOM_START_DATE"]
                for field in date_fields:
                    if field in issue_data and isinstance(issue_data[field], str):
                        try:
                            from datetime import datetime

                            issue_data[field] = datetime.strptime(
                                issue_data[field], "%Y-%m-%d"
                            ).date()
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


class IssueCreate(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    audit_id: Optional[int] = None
    resolve_at: Optional[str] = None
    due_date: Optional[str] = None
    votes: Optional[int] = None
    original_estimation: Optional[int] = None
    custom_start_date: Optional[str] = None
    story_point_estimate: Optional[int] = None
    parent_summary: Optional[int] = None
    issue_type: Optional[int] = None
    project_id_fk: Optional[int] = None
    user_assigned_fk: Optional[int] = None
    user_creator_issue_fk: Optional[int] = None
    user_informator_fk: Optional[int] = None
    sprint_id_fk: Optional[int] = None
    status_issue: Optional[int] = None

class IssuePatchRequest(BaseModel):
    issue_id: int
    summary: Optional[str] = None
    description: Optional[str] = None
    audit_id: Optional[int] = None
    resolve_at: Optional[date] = None
    due_date: Optional[date] = None
    votes: Optional[int] = None
    original_estimation: Optional[int] = None
    custom_start_date: Optional[date] = None
    story_point_estimate: Optional[int] = None
    parent_summary: Optional[int] = None
    issue_type: Optional[int] = None
    project_id: Optional[int] = None
    user_assigned: Optional[int] = None
    user_creator: Optional[int] = None
    user_informator: Optional[int] = None
    sprint_id: Optional[int] = None
    status: Optional[int] = None
    
    
class IssuePutRequest(BaseModel):
    issue_id: int
    summary: str
    description: str
    audit_id: int
    resolve_at: date
    due_date: date
    votes: int
    original_estimation: int
    custom_start_date: date
    story_point_estimate: int
    parent_summary: int
    issue_type: int
    project_id: int
    user_assigned: int
    user_creator: int
    user_informator: int
    sprint_id: int
    status: int