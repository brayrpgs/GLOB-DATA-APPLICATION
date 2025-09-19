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
    data: List[Dict[str, Any]]  # Raw JSON from the SP
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
                logger.warning("Error validating sprint: %s, data: %s", e, item)
        return validated

class SprintCreate(BaseModel):
    name: str = Field(..., description="Name of the sprint")
    description: str = Field(..., description="Description of the sprint")
    date_init: date = Field(..., description="Start date of the sprint")
    date_end: date = Field(..., description="End date of the sprint")

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
