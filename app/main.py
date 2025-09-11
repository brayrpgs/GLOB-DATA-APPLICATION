from fastapi import FastAPI
from app.api import items

app = FastAPI(title="Mi API")

app.include_router(items.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Hello World"}
