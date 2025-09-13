from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, validator
from datetime import datetime

class Issue(BaseModel):
    ISSUE_ID: Optional[int] = Field(None, alias="ISSUE_ID")
    SUMMARY: Optional[str] = Field(None, alias="SUMMARY")
    DESCRIPTION: Optional[str] = Field(None, alias="DESCRIPTION")
    AUDIT_ID_FK: Optional[int] = Field(None, alias="AUDIT_ID_FK")
    RESOLVE_AT: Optional[date] = Field(None, alias="RESOLVE_AT")
    DUE_DATE: Optional[date] = Field(None, alias="DUE_DATE")
    VOTES: Optional[int] = Field(None, alias="VOTES")
    ORIGINAL_ESTIMATION: Optional[int] = Field(None, alias="ORIGINAL_ESTIMATION")
    CUSTOM_START_DATE: Optional[date] = Field(None, alias="CUSTOM_START_DATE")
    STORY_POINT_ESTIMATE: Optional[int] = Field(None, alias="STORY_POINT_ESTIMATE")
    PARENT_SUMMARY_FK: Optional[int] = Field(None, alias="PARENT_SUMMARY_FK")
    ISSUE_TYPE: Optional[int] = Field(None, alias="ISSUE_TYPE")
    PROJECT_ID_FK: Optional[int] = Field(None, alias="PROJECT_ID_FK")
    USER_ASSIGNED_FK: Optional[int] = Field(None, alias="USER_ASSIGNED_FK")
    USER_CREATOR_ISSUE_FK: Optional[int] = Field(None, alias="USER_CREATOR_ISSUE_FK")
    # Corregido el nombre del campo para que coincida con el JSON del SP
    USER_INFORMATOR_ISSUE_FK: Optional[int] = Field(None, alias="USER_INFORMATOR_ISSUE_FK")
    SPRINT_ID_FK: Optional[int] = Field(None, alias="SPRINT_ID_FK")
    STATUS_ISSUE: Optional[int] = Field(None, alias="STATUS_ISSUE")

    @validator('RESOLVE_AT', 'DUE_DATE', 'CUSTOM_START_DATE', pre=True)
    def parse_date(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                # Si no se puede parsear, devolver None o lanzar error
                return None
        return v

    class Config:
        allow_population_by_field_name = True
        # Permitir usar alias para la población
        populate_by_name = True