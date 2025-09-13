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
        raise HTTPException(status_code=400, detail=f"Formato de fecha inválido: {value}")
    
def _validate_pagination_parameters(page: int, limit: int) -> None:
    """
    Valida los parámetros de paginación.
    
    Args:
        page: Número de página
        limit: Límite de resultados por página
        
    Raises:
        HTTPException: Si los parámetros no son válidos
    """
    if page < 1:
        raise HTTPException(
            status_code=400, 
            detail="El parámetro 'page' debe ser mayor a 0"
        )
    
    if limit < 1 or limit > 100:  # Límite máximo configurable
        raise HTTPException(
            status_code=400, 
            detail="El parámetro 'limit' debe estar entre 1 y 100"
        )