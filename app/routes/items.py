from fastapi import APIRouter
from app.schemas.item import Item
from typing import List

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello from items router"}

@router.get("/items", response_model=List[Item])
def read_items():
    return [
        {"id": 1, "name": "Item 1", "description": "This is item 1"},
        {"id": 2, "name": "Item 2", "description": "This is item 2"},
    ]
