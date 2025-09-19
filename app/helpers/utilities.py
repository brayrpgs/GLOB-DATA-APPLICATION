from datetime import datetime, date
from typing import Optional
from fastapi import HTTPException

def parse_date(value: Optional[str]) -> Optional[date]:
    if value is None:
        return None
    try:
        #parsing the date
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {value}")
    
def parse_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid integer format: {value}"
        )
    
def _validate_pagination_parameters(page: int, limit: int) -> None:
    """
    Validates pagination parameters.
    
    Args:
        page: Page number
        limit: Results limit per page
        
    Raises:
        HTTPException: If the parameters are not valid
    """
    if page < 1:
        raise HTTPException(
            status_code=401, 
            detail="The 'page' parameter must be greater than 0"
        )
    
    if limit < 1 or limit > 100:  # Configurable maximum limit
        raise HTTPException(
            status_code=402, 
            detail="The 'limit' parameter must be between 1 and 100"
        )