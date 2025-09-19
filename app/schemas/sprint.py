from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

class Sprint(BaseModel):
    sprint_id: Optional[int] = Field(None, alias="SPRINT_ID")
    name: Optional[str] = Field(None, alias="NAME")
    description: Optional[str] = Field(None, alias="DESCRIPTION")
    date_init: Optional[date] = Field(None, alias="DATE_INIT")
    date_end: Optional[date] = Field(None, alias="DATE_END")

    class Config:
        allow_population_by_field_name = True

class SprintResponse(BaseModel):
    data: List[Dict[str, Any]]  # JSON raw del SP
    page: Optional[int]
    currentLimit: Optional[int]

    def get_validated_sprints(self) -> List[Sprint]:
        validated = []
        for item in self.data:
            try:
                for field in ["DATE_INIT", "DATE_END"]:
                    if field in item and isinstance(item[field], str):
                        item[field] = datetime.strptime(item[field], "%Y-%m-%d").date()
                validated.append(Sprint(**item))
            except Exception as e:
                logger.warning("Error al validar sprint: %s, data: %s", e, item)
        return validated

class SprintCreate(BaseModel):
    name: str = Field(..., description="Nombre del sprint")
    description: str = Field(..., description="Descripción del sprint")
    date_init: date = Field(..., description="Fecha de inicio del sprint")
    date_end: date = Field(..., description="Fecha de fin del sprint")

class SprintPatchRequest(BaseModel):
    sprint_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    date_init: Optional[date] = None
    date_end: Optional[date] = None

class SprintPutRequest(BaseModel):
    sprint_id: int
    name: str
    description: str
    date_init: date
    date_end: date
