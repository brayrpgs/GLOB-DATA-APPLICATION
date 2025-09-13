from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.issues_routes import router as issue_router
from app.database.conection import init_pool, close_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar
    await init_pool()
    yield

app = FastAPI(title="API de Issues", lifespan=lifespan)

# Montar routers
app.include_router(issue_router)
